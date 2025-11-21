"""
振り仮名変換ユーティリティ
カッコ形式の振り仮名をHTMLルビタグに変換
"""

import re


def convert_furigana_to_ruby(text: str) -> str:
    """
    カッコ形式の振り仮名をHTMLルビタグに変換

    例:
        在留(ざいりゅう)カード → <ruby>在留<rt>ざいりゅう</rt></ruby>カード
        市役所(しやくしょ) → <ruby>市役所<rt>しやくしょ</rt></ruby>

    Args:
        text: 変換対象のテキスト（カッコ形式の振り仮名を含む）

    Returns:
        HTMLルビタグに変換されたテキスト
    """
    # パターン: 漢字(ひらがな)
    # 漢字は一文字以上、ひらがなは一文字以上
    pattern = r'([一-龠々〆ヵヶ]+)\(([ぁ-ん]+)\)'

    # 置換: <ruby>漢字<rt>ひらがな</rt></ruby>
    ruby_text = re.sub(pattern, r'<ruby>\1<rt>\2</rt></ruby>', text)

    return ruby_text


def remove_furigana(text: str) -> str:
    """
    テキストから振り仮名を削除（カッコとその中身を削除）

    例:
        在留(ざいりゅう)カード → 在留カード

    Args:
        text: 振り仮名を含むテキスト

    Returns:
        振り仮名を削除したテキスト
    """
    # カッコとその中身を削除
    pattern = r'\([ぁ-ん]+\)'
    clean_text = re.sub(pattern, '', text)

    return clean_text


def extract_furigana_pairs(text: str) -> list[tuple[str, str]]:
    """
    テキストから漢字と振り仮名のペアを抽出

    例:
        "在留(ざいりゅう)カードを市役所(しやくしょ)へ"
        → [("在留", "ざいりゅう"), ("市役所", "しやくしょ")]

    Args:
        text: 振り仮名を含むテキスト

    Returns:
        (漢字, 振り仮名)のタプルのリスト
    """
    pattern = r'([一-龠々〆ヵヶ]+)\(([ぁ-ん]+)\)'
    matches = re.findall(pattern, text)

    return matches


def format_text_with_ruby_html(text: str, line_height: float = 2.0) -> str:
    """
    振り仮名付きテキストをHTMLフォーマットに変換（表示用）

    Args:
        text: カッコ形式の振り仮名を含むテキスト
        line_height: 行間（デフォルト: 2.0）

    Returns:
        スタイル付きHTMLテキスト
    """
    ruby_text = convert_furigana_to_ruby(text)

    # 改行を<br>タグに変換
    ruby_text = ruby_text.replace('\n', '<br>')

    # スタイル付きHTMLを生成
    html = f"""
<div style="
    font-size: 1.1rem;
    line-height: {line_height};
    padding: 1rem;
    background-color: #f8f9fa;
    border-radius: 8px;
    border-left: 4px solid #1E88E5;
">
{ruby_text}
</div>
"""

    return html


if __name__ == "__main__":
    # テスト用
    test_text = """日本に入った人で、在留(ざいりゅう)カード（外国人が持つカード）をもらった人は、次のことをしてください。

・住む場所を決めます
・決めた日から14日以内に手続(てつづ)きをします
・在留(ざいりゅう)カードを持って、市役所(しやくしょ)か区役所(くやくしょ)に行きます
・「転入届(てんにゅうとどけ)」という紙を出します"""

    print("=" * 80)
    print("カッコ形式:")
    print("=" * 80)
    print(test_text)
    print()

    print("=" * 80)
    print("HTMLルビ形式:")
    print("=" * 80)
    ruby_html = convert_furigana_to_ruby(test_text)
    print(ruby_html)
    print()

    print("=" * 80)
    print("振り仮名削除:")
    print("=" * 80)
    clean_text = remove_furigana(test_text)
    print(clean_text)
    print()

    print("=" * 80)
    print("振り仮名ペア抽出:")
    print("=" * 80)
    pairs = extract_furigana_pairs(test_text)
    for kanji, reading in pairs:
        print(f"{kanji} → {reading}")
