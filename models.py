"""Model initialization and management for DeepSeek models"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from deepseek_vl.models import VLChatProcessor, MultiModalityCausalLM
from config import CODE_MODEL_ID, VL_MODEL_PATH


class ModelManager:
    """Manages the initialization and access to both code generation and vision-language models"""
    
    def __init__(self):
        self.code_model = None
        self.code_tokenizer = None
        self.vl_model = None
        self.vl_chat_processor = None
        self.vl_tokenizer = None
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize both code generation and vision-language models"""
        self._initialize_code_model()
        self._initialize_vl_model()
    
    def _initialize_code_model(self):
        """Initialize the code generation model"""
        print("Loading code generation model...")
        self.code_model = AutoModelForCausalLM.from_pretrained(CODE_MODEL_ID)
        self.code_tokenizer = AutoTokenizer.from_pretrained(CODE_MODEL_ID)
        self.code_model.eval()
        
        if torch.cuda.is_available():
            self.code_model.to("cuda")
            print("Code model moved to CUDA")
    
    def _initialize_vl_model(self):
        """Initialize the vision-language model"""
        print("Loading vision-language model...")
        self.vl_chat_processor = VLChatProcessor.from_pretrained(VL_MODEL_PATH)
        self.vl_tokenizer = self.vl_chat_processor.tokenizer
        self.vl_model = AutoModelForCausalLM.from_pretrained(
            VL_MODEL_PATH,
            trust_remote_code=True
        )
        self.vl_model.eval()
        
        # Move to bfloat16 and GPU if available
        self.vl_model = self.vl_model.to(torch.bfloat16)
        if torch.cuda.is_available():
            self.vl_model = self.vl_model.to("cuda")
            print("Vision-language model moved to CUDA")
    
    def get_code_model(self):
        """Get code generation model and tokenizer"""
        return self.code_model, self.code_tokenizer
    
    def get_vl_model(self):
        """Get vision-language model, processor, and tokenizer"""
        return self.vl_model, self.vl_chat_processor, self.vl_tokenizer


# Global model manager instance
model_manager = ModelManager()