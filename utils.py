"""Utility functions for text processing and cleaning"""

import re


def clean_generated_output(code: str) -> str:
    """Comprehensive cleaning of generated code output"""
    # Remove the specific unwanted instruction text
    code = re.sub(
        r'Include any necessary imports and ensure the snippet is functional\.?\s*',
        '', 
        code,
        flags=re.IGNORECASE
    )
    
    # Remove special tokens and thinking blocks
    code = re.sub(r'<\|.*?\|>', '', code, flags=re.DOTALL)
    code = re.sub(r'</?think>', '', code, flags=re.IGNORECASE)
    
    # Remove code fences and the word "python" in any context
    code = re.sub(r'```\s*(python)?\s*|```', '', code, flags=re.IGNORECASE)
    code = re.sub(r'\bpython\b', '', code, flags=re.IGNORECASE)
    
    # Remove empty lines at start and end
    return re.sub(r'^\s*\n+|\n+\s*$', '', code).strip()