"""Code generation and image description functions"""

import torch
from models import model_manager
from utils import clean_generated_output
from prompting import create_code_generation_messages, create_image_conversation
from config import DEFAULT_CODE_PARAMS, DEFAULT_IMAGE_PARAMS


def generate_code_snippet(
    user_prompt: str,
    max_new_tokens: int = DEFAULT_CODE_PARAMS["max_new_tokens"],
    temperature: float = DEFAULT_CODE_PARAMS["temperature"],
    top_p: float = DEFAULT_CODE_PARAMS["top_p"],
    top_k: int = DEFAULT_CODE_PARAMS["top_k"]
) -> str:
    """Enhanced code generation with adjustable parameters"""
    
    # Get models
    code_model, code_tokenizer = model_manager.get_code_model()
    
    # Create messages
    messages = create_code_generation_messages(user_prompt)
    
    # Apply chat template
    text_input = code_tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        continue_final_message=True
    )

    # Tokenize and generate
    model_inputs = code_tokenizer([text_input], return_tensors="pt")
    if torch.cuda.is_available():
        model_inputs = {k: v.to("cuda") for k, v in model_inputs.items()}

    generated_output = code_model.generate(
        **model_inputs,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        do_sample=True,
    )

    batch_input_ids = model_inputs["input_ids"]
    generated_ids = [
        output_ids[len(input_ids):]
        for input_ids, output_ids in zip(batch_input_ids, generated_output)
    ]

    # Decode and clean
    generated_snippet = code_tokenizer.batch_decode(
        generated_ids, 
        skip_special_tokens=True
    )[0]

    return clean_generated_output(generated_snippet)


def generate_image_description(
    image,
    max_new_tokens: int = DEFAULT_IMAGE_PARAMS["max_new_tokens"],
    temperature: float = DEFAULT_IMAGE_PARAMS["temperature"],
    top_p: float = DEFAULT_IMAGE_PARAMS["top_p"],
    top_k: int = DEFAULT_IMAGE_PARAMS["top_k"],
    detail_level: str = DEFAULT_IMAGE_PARAMS["detail_level"]
) -> str:
    """Enhanced image description with adjustable parameters"""
    
    # Get models
    vl_model, vl_chat_processor, vl_tokenizer = model_manager.get_vl_model()
    
    # Build conversation
    conversation = create_image_conversation(detail_level)
    
    # Prepare inputs
    pil_images = [image]
    prepared = vl_chat_processor(
        conversations=conversation,
        images=pil_images,
        force_batchify=True
    ).to(vl_model.device)
    
    # Generate description
    inputs_embeds = vl_model.prepare_inputs_embeds(**prepared)
    output_ids = vl_model.language_model.generate(
        inputs_embeds=inputs_embeds,
        attention_mask=prepared.attention_mask,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        do_sample=True,
        pad_token_id=vl_tokenizer.eos_token_id,
        eos_token_id=vl_tokenizer.eos_token_id
    )
    
    # Decode and clean
    description = vl_tokenizer.decode(
        output_ids[0].cpu().tolist(), 
        skip_special_tokens=True
    )
    return description.strip()