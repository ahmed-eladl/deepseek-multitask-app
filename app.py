"""Main application file for DeepSeek Multi-Task Application"""

import gradio as gr
from config import APP_TITLE, APP_DESCRIPTION
from ui_components import create_code_generation_tab, create_image_description_tab, create_theme


def create_app():
    """Create and configure the main Gradio application"""
    theme = create_theme()
    
    with gr.Blocks(title=APP_TITLE, theme=theme) as app:
        gr.Markdown(APP_DESCRIPTION)
        
        with gr.Tabs():
            create_code_generation_tab()
            create_image_description_tab()
    
    return app


def main():
    """Main function to launch the application"""
    app = create_app()
    app.launch(share=True)


if __name__ == "__main__":
    main()