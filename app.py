"""
やさしい日本語翻訳ツール - Streamlitアプリ
文化庁「在留支援のためのやさしい日本語ガイドライン」に準拠
"""

import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
from typing import Optional
import config
from prompt_builder import build_system_message, build_user_message
from furigana_utils import convert_furigana_to_ruby, format_text_with_ruby_html

# 環境変数を読み込む
load_dotenv()


# ページ設定
st.set_page_config(
    page_title="やさしい日本語翻訳ツール",
    page_icon="🗣️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #616161;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        padding: 0.5rem;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #1565C0;
    }
    .sample-button {
        margin: 0.2rem 0;
    }
    .result-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #f5f5f5;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def get_groq_client() -> Optional[Groq]:
    """
    Groq APIクライアントを取得

    Returns:
        Groqクライアント、または None（エラー時）
    """
    try:
        # 環境変数からAPIキーを取得、なければデモキーを使用
        api_key = os.getenv("GROQ_API_KEY", config.DEMO_API_KEY)

        if not api_key or api_key == "gsk_YOUR_DEMO_KEY_HERE":
            st.error("⚠️ GROQ_API_KEYが設定されていません。環境変数に設定してください。")
            st.info("💡 Groq APIキーは https://console.groq.com から取得できます。")
            return None

        return Groq(api_key=api_key)
    except Exception as e:
        st.error(f"❌ Groq APIクライアントの初期化に失敗しました: {str(e)}")
        return None


def translate_to_yasashii(text: str, client: Groq) -> Optional[str]:
    """
    通常の日本語を「やさしい日本語」に翻訳

    Args:
        text: 変換対象のテキスト
        client: GroqクライアントReturns:
        変換後のテキスト、または None（エラー時）
    """
    try:
        # プロンプトを構築（品質向上のため8個の例を使用）
        system_message = build_system_message()
        user_message = build_user_message(text, num_examples=8)

        # Groq APIを呼び出し
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            model=config.MODEL_NAME,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS,
        )

        # 結果を取得
        result = chat_completion.choices[0].message.content.strip()
        return result

    except Exception as e:
        st.error(f"❌ 翻訳中にエラーが発生しました: {str(e)}")
        return None


def main():
    """メインアプリケーション"""

    # ヘッダー
    st.markdown('<div class="main-header">🗣️ やさしい日本語翻訳ツール</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">文化庁ガイドライン準拠 - 外国人にもわかりやすい日本語に変換</div>', unsafe_allow_html=True)

    # サイドバー
    with st.sidebar:
        st.header("📋 使い方")
        st.markdown("""
        1. **テキストを入力**
           変換したい日本語を入力してください

        2. **サンプルを試す**
           サンプルボタンで例文を試せます

        3. **変換ボタンをクリック**
           「やさしい日本語」に変換します
        """)

        st.divider()

        # ガイドライン説明
        with st.expander("📖 やさしい日本語とは？"):
            st.markdown("""
            **やさしい日本語**は、日本語に不慣れな外国人にも
            わかりやすい日本語のことです。

            **主なルール:**
            - 一文を短くする（20〜30文字）
            - 簡単な言葉を使う
            - 箇条書きを活用する
            - 二重否定を避ける
            - 具体的に書く

            文化庁の「在留支援のためのやさしい日本語
            ガイドライン」に準拠しています。
            """)

        with st.expander("🎯 対象ユーザー"):
            st.markdown("""
            このツールは以下の方を対象としています:

            - **CEFR C1-2レベル**の日本語学習者
            - 生活者としての外国人
            - 日本での生活情報を必要とする方
            """)

        st.divider()
        st.caption("Powered by Groq + Llama 3.1")

    # メインコンテンツ
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📝 通常の日本語")

        # サンプルボタン（テキストエリアの前に配置）
        st.markdown("**📌 サンプルを試す:**")
        sample_cols = st.columns(5)

        for idx, (category, sample_text) in enumerate(config.SAMPLE_TEXTS.items()):
            with sample_cols[idx]:
                if st.button(category, key=f"sample_{category}", use_container_width=True):
                    st.session_state.input_text = sample_text
                    st.rerun()

        # session_stateの初期化
        if "input_text" not in st.session_state:
            st.session_state.input_text = ""

        # テキスト入力エリア
        input_text = st.text_area(
            "変換したいテキストを入力してください",
            height=300,
            placeholder="ここに変換したい日本語を入力してください...",
            key="input_text"
        )

        # 変換ボタン
        st.divider()
        convert_button = st.button("🔄 やさしい日本語に変換", type="primary", use_container_width=True)

    with col2:
        st.subheader("✨ やさしい日本語")

        # 初期表示
        if "translated_text" not in st.session_state:
            st.session_state.translated_text = ""

        if st.session_state.translated_text:
            # 振り仮名付きHTML表示
            ruby_html = format_text_with_ruby_html(st.session_state.translated_text)
            st.markdown(ruby_html, unsafe_allow_html=True)

            # ダウンロードボタン
            st.divider()
            download_cols = st.columns(2)

            with download_cols[0]:
                # カッコ版のダウンロード
                st.download_button(
                    label="📥 カッコ版をダウンロード",
                    data=st.session_state.translated_text,
                    file_name="yasashii_nihongo.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            with download_cols[1]:
                # HTMLルビ版のダウンロード
                ruby_html_download = convert_furigana_to_ruby(st.session_state.translated_text)
                html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>やさしい日本語</title>
    <style>
        body {{
            font-family: 'Noto Sans JP', sans-serif;
            line-height: 2.0;
            padding: 2rem;
            max-width: 800px;
            margin: 0 auto;
        }}
        ruby {{
            ruby-position: over;
        }}
        rt {{
            font-size: 0.6em;
        }}
    </style>
</head>
<body>
    <h1>やさしい日本語</h1>
    <p>{ruby_html_download.replace(chr(10), '<br>')}</p>
</body>
</html>"""
                st.download_button(
                    label="📥 HTML版をダウンロード",
                    data=html_content,
                    file_name="yasashii_nihongo.html",
                    mime="text/html",
                    use_container_width=True
                )
        else:
            st.info("👈 左側でテキストを入力し、変換ボタンをクリックしてください")

    # 変換処理
    if convert_button:
        if not input_text or input_text.strip() == "":
            st.warning("⚠️ テキストを入力してください")
        else:
            # Groqクライアントを取得
            client = get_groq_client()

            if client:
                with st.spinner("🔄 変換中..."):
                    # 翻訳実行
                    translated = translate_to_yasashii(input_text, client)

                    if translated:
                        st.session_state.translated_text = translated
                        st.success("✅ 変換が完了しました！")
                        st.rerun()

    # フッター
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #616161; font-size: 0.9rem;">
        文化庁「在留支援のためのやさしい日本語ガイドライン」準拠<br>
        Llama Hackathon Project | Powered by Groq + Llama 3.3
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
