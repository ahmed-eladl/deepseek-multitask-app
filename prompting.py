"""Prompt management functions for code generation and image description"""

from config import DETAIL_PROMPTS


def create_code_generation_messages(user_prompt: str) -> list:
    """Create the message structure for code generation"""
    # System message
    system_message = {
        "role": "system",
        "content": (
            "You are a code-generation AI. When given a prompt, "
            "you must return only the Python code snippet that fulfills the request. "
            "Do NOT include any explanations, JSON schemas, commentary, or special tokens."
        )
    }

    # Example user-assistant interaction (to prime the model)
    user_assistant_message = {
        "role": "user",
        "content": (
            "Generate a Python code snippet that fulfills this request:\n\n"
            "\"\"\"\n"
            "Create a Python function to calculate Fibonacci sequence with O(n) time complexity\n"
            "\"\"\"\n"
            "Include any necessary imports and ensure the snippet is functional."
        )
    }

    assistant_message = {
        "role": "assistant",
        "content": (
            """
            def fibonacci(n):
                if n == 0:
                    return 0
                elif n == 1:
                    return 1
                elif n == 2:
                    return 1
                else:
                    a, b = 0, 1
                    for i in range(2, n):
                        a, b = b, a + b
                    return b
            
            n = int(input("Enter the number of the Fibonacci sequence: "))
            print(fibonacci(n))
            """
        )
    }

    # Actual user prompt
    user_message = {
        "role": "user",
        "content": (
            f"Generate a Python code snippet that fulfills this request:\n\n"
            f"\"\"\"\n{user_prompt}\n\"\"\"\n"
        )
    }

    return [system_message, user_assistant_message, assistant_message, user_message]


def create_image_conversation(detail_level: str) -> list:
    """Create conversation structure for image description"""
    detail_prompt = DETAIL_PROMPTS.get(detail_level, "Describe in detail.")
    
    return [
        {"role": "User", "content": f"<image_placeholder> {detail_prompt}"},
        {"role": "Assistant", "content": ""}
    ]