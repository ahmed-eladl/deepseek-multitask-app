"""UI components for the Gradio interface"""

import gradio as gr
from generators import generate_code_snippet, generate_image_description


def create_code_generation_tab():
    """Create the code generation tab"""
    with gr.TabItem("🧑‍💻 Code Generation (DeepSeek-R1-Distill-Qwen-1.5B)"):
        gr.Markdown("### Python Code Generation using DeepSeek-R1-Distill-Qwen-1.5B\n"
            "Transform natural language requests into functional Python code snippet.")
        
        with gr.Row():
            with gr.Column(scale=3):
                prompt_input = gr.Textbox(
                    label="Code Request",
                    placeholder="e.g., Create a Python function to calculate factorial of a number",
                    value="Create a Python function to calculate Fibonacci sequence with O(n) time complexity",  
                    lines=4
                )
                with gr.Accordion("⚙️ Generation Parameters", open=False):
                    with gr.Row():
                        max_tokens = gr.Slider(100, 2048, value=512, label="Max Tokens")
                        temperature = gr.Slider(0.1, 1.0, value=0.6, step=0.1, label="Temperature")
                    with gr.Row():
                        top_p = gr.Slider(0.1, 1.0, value=0.9, step=0.1, label="Top-p")
                        top_k = gr.Slider(1, 100, value=50, step=1, label="Top-k")
                
                generate_btn = gr.Button("Generate Code", variant="primary")
            
            with gr.Column(scale=2):
                code_output = gr.Textbox(
                    label="Generated Python Code",
                    lines=20,
                )
        
        generate_btn.click(
            fn=generate_code_snippet,
            inputs=[prompt_input, max_tokens, temperature, top_p, top_k],
            outputs=code_output
        )


def create_image_description_tab():
    """Create the image description tab"""
    with gr.TabItem("🖼️ Image Description (deepseek-vl-1.3b-chat)"):
        gr.Markdown("### Image Description using deepseek-vl-1.3b-chat\n"
            "Generate detailed descriptions from uploaded images.")
        
        with gr.Row():
            with gr.Column(scale=1):
                image_input = gr.Image(
                    type="pil",
                    label="Upload Image",
                    sources=["upload", "clipboard"]
                )
                with gr.Accordion("⚙️ Description Parameters", open=False):
                    detail_level = gr.Radio(
                        ["Concise", "Detailed", "Extreme"],
                        value="Detailed",
                        label="Detail Level"
                    )
                    with gr.Row():
                        img_max_tokens = gr.Slider(100, 2048, value=512, label="Max Tokens")
                        img_temp = gr.Slider(0.1, 1.0, value=0.6, step=0.1, label="Temperature")
                    with gr.Row():
                        img_top_p = gr.Slider(0.1, 1.0, value=0.9, step=0.1, label="Top-p")
                        img_top_k = gr.Slider(1, 100, value=50, step=1, label="Top-k")
                
                describe_btn = gr.Button("Describe Image", variant="primary")
            
            with gr.Column(scale=2):
                description_output = gr.Textbox(
                    label="Image Description",
                    lines=20,
                )
        
        describe_btn.click(
            fn=generate_image_description,
            inputs=[image_input, img_max_tokens, img_temp, img_top_p, img_top_k, detail_level],
            outputs=description_output
        )


def create_theme():
    """Create and return the Gradio theme"""
    return gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="gray",
        font=[gr.themes.GoogleFont("Inter"), "sans-serif"]
    )