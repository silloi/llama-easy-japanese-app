"""
やさしい日本語翻訳ツール - プロンプト構築モジュール
文化庁ガイドラインに基づいたプロンプトを生成
"""

import random
from typing import List, Dict
from config import SYSTEM_PROMPT, GUIDELINE_RULES, FEW_SHOT_EXAMPLES


def build_prompt(user_input: str, num_examples: int = 5) -> str:
    """
    文化庁ガイドラインに基づいたプロンプトを構築

    Args:
        user_input: 変換対象の日本語テキスト
        num_examples: 使用するFew-shot examplesの数（デフォルト: 5）

    Returns:
        完全なプロンプト文字列
    """
    # Few-shot examplesから指定数をランダムに選択（多様性のため）
    selected_examples = FEW_SHOT_EXAMPLES[:num_examples]  # 最初のN個を使用

    # Few-shot examplesのフォーマット
    examples_text = format_examples(selected_examples)

    # 完全なプロンプトを構築
    full_prompt = f"""{SYSTEM_PROMPT}

{GUIDELINE_RULES}

【変換例】
{examples_text}

【変換対象】
以下の文章を「やさしい日本語」に変換してください。

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
        formatted.append(f"""例{i}:
原文: {example['original']}
やさしい日本語: {example['yasashii']}
""")

    return "\n".join(formatted)


def build_system_message() -> str:
    """
    システムメッセージを構築（Groq API用）

    Returns:
        システムメッセージ
    """
    return SYSTEM_PROMPT


def build_user_message(user_input: str, num_examples: int = 5) -> str:
    """
    ユーザーメッセージを構築（Groq API用）

    Args:
        user_input: 変換対象の日本語テキスト
        num_examples: 使用するFew-shot examplesの数

    Returns:
        ユーザーメッセージ
    """
    selected_examples = FEW_SHOT_EXAMPLES[:num_examples]
    examples_text = format_examples(selected_examples)

    user_message = f"""{GUIDELINE_RULES}

【変換例】
{examples_text}

【変換対象】
以下の文章を「やさしい日本語」に変換してください。

原文:
{user_input}

やさしい日本語:"""

    return user_message


if __name__ == "__main__":
    # テスト用
    test_input = "新規の上陸許可を受けて日本に入国した場合、在留カードが交付された方は、住所を定めた日から14日以内に、在留カードをお持ちになってお住まいの市町村において転入の届出をする必要があります。"

    prompt = build_prompt(test_input, num_examples=3)
    print("=" * 80)
    print("生成されたプロンプト:")
    print("=" * 80)
    print(prompt)
    print("=" * 80)
