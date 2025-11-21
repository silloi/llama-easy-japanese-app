"""
やさしい日本語翻訳ツール - プロンプト構築モジュール
文化庁ガイドラインに基づいたプロンプトを生成
"""

import random
from typing import List, Dict
from config import SYSTEM_PROMPT, GUIDELINE_RULES, FEW_SHOT_EXAMPLES


def build_prompt(user_input: str, num_examples: int = 8) -> str:
    """
    文化庁ガイドラインに基づいたプロンプトを構築

    Args:
        user_input: 変換対象の日本語テキスト
        num_examples: 使用するFew-shot examplesの数（デフォルト: 8）

    Returns:
        完全なプロンプト文字列
    """
    # Few-shot examplesから指定数を使用（品質向上のため多めに）
    selected_examples = FEW_SHOT_EXAMPLES[:num_examples]

    # Few-shot examplesのフォーマット
    examples_text = format_examples(selected_examples)

    # 完全なプロンプトを構築
    full_prompt = f"""{SYSTEM_PROMPT}

{GUIDELINE_RULES}

【変換例】
以下の例を参考に、同じパターンで変換してください。

{examples_text}

【変換対象】
以下の文章を「やさしい日本語」に変換してください。
上記のルールをすべて適用し、変換後のテキストのみを出力してください。

原文:
{user_input}

やさしい日本語:"""

    return full_prompt


def format_examples(examples: List[Dict[str, str]]) -> str:
    """
    Few-shot examplesを読みやすい形式にフォーマット

    Args:
        examples: 変換例のリスト

    Returns:
        フォーマットされた例文の文字列
    """
    formatted = []

    for i, example in enumerate(examples, 1):
        formatted.append(f"""【例{i}】
原文:
{example['original']}

やさしい日本語:
{example['yasashii']}
""")

    return "\n".join(formatted)


def build_system_message() -> str:
    """
    システムメッセージを構築（Groq API用）

    Returns:
        システムメッセージ
    """
    return SYSTEM_PROMPT


def build_user_message(user_input: str, num_examples: int = 8) -> str:
    """
    ユーザーメッセージを構築（Groq API用）

    Args:
        user_input: 変換対象の日本語テキスト
        num_examples: 使用するFew-shot examplesの数（デフォルト: 8）

    Returns:
        ユーザーメッセージ
    """
    # Few-shot examplesを選択（品質向上のため多めに使用）
    selected_examples = FEW_SHOT_EXAMPLES[:num_examples]
    examples_text = format_examples(selected_examples)

    user_message = f"""{GUIDELINE_RULES}

【変換例】
以下の例を参考に、同じパターンで変換してください。
特に注意：
- 一文は20〜30文字程度に短くする
- 複数の情報は必ず箇条書き（・）にする
- 受動態は能動態に変換する
- 敬語は「です・ます」のみ使用
- 難しい言葉には説明を添える

{examples_text}

【変換対象】
以下の文章を「やさしい日本語」に変換してください。
上記のルールをすべて適用し、変換後のテキストのみを出力してください。

原文:
{user_input}

やさしい日本語:"""

    return user_message


if __name__ == "__main__":
    # テスト用
    test_input = "新規の上陸許可を受けて日本に入国した場合、在留カードが交付された方は、住所を定めた日から14日以内に、在留カードをお持ちになってお住まいの市町村において転入の届出をする必要があります。"

    prompt = build_prompt(test_input, num_examples=5)
    print("=" * 80)
    print("生成されたプロンプト:")
    print("=" * 80)
    print(prompt)
    print("=" * 80)
