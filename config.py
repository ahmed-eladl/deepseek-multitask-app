"""Configuration settings for the DeepSeek Multi-Task Application"""

# Model configurations
CODE_MODEL_ID = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
VL_MODEL_PATH = "deepseek-ai/deepseek-vl-1.3b-chat"

# Default generation parameters
DEFAULT_CODE_PARAMS = {
    "max_new_tokens": 1500,
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 50
}

DEFAULT_IMAGE_PARAMS = {
    "max_new_tokens": 512,
    "temperature": 0.5,
    "top_p": 0.9,
    "top_k": 50,
    "detail_level": "Detailed"
}

# UI Configuration
APP_TITLE = "DeepSeek Multi-Task App"
APP_DESCRIPTION = """
# 🚀 DeepSeek Multi-Model Application
*Code Generation with DeepSeek-R1-Distill-Qwen-1.5B & Image Description with deepseek-vl-1.3b-chat*
"""

# Detail level prompts for image description
DETAIL_PROMPTS = {
    "Concise": "Describe an image concisely.",
    "Detailed": "Describe an image in detail.",
    "Extreme": "Describe every visible detail exhaustively of this image."
}