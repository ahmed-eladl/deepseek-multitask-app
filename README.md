# DeepSeek Multi-Task App

A Gradio‐based interface that combines two powerful functionalities in one application:

1. **Code Generation** using the DeepSeek-R1-Distill-Qwen-1.5B model  
2. **Image Description** using the deepseek-vl-1.3b-chat model

This README provides step‐by‐step setup instructions, detailed usage guidelines, and illustrative examples for both modules.

---

## Table of Contents

- [Features](#features)  
- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [Model Downloads & Configuration](#model-downloads--configuration)  
- [Running the App](#running-the-app)  
- [Usage Guidelines](#usage-guidelines)  
  - [1. Code Generation Tab](#1-code-generation-tab)  
  - [2. Image Description Tab](#2-image-description-tab)  
- [Examples](#examples)  
  - [Code Generation Examples](#code-generation-examples)  
  - [Image Description Examples](#image-description-examples)  
- [Project Structure](#project-structure)  
- [Troubleshooting](#troubleshooting)  
- [Contributing](#contributing)  
- [License](#license)  

---

## Features

- **Code Generation**  
  - Generates Python code snippets from natural language prompts.  
  - Adjustable generation parameters:  
    - Maximum tokens (`max_new_tokens`)  
    - Temperature  
    - Top-p (nucleus sampling)  
    - Top-k (top-k sampling)  

- **Image Description**  
  - Produces detailed (or concise/extreme) descriptions of user‐uploaded images.  
  - Adjustable generation parameters:  
    - Maximum tokens (`max_new_tokens`)  
    - Temperature  
    - Top-p  
    - Top-k  

- **Gradio Interface**  
  - Intuitive UI with two separate tabs.  
  - Sliders, radio buttons, and text boxes to control generation.  
  - Live inference on CUDA (if available).  

---

## Prerequisites

1. **Operating System**: Linux, macOS, or Windows (Windows Subsystem for Linux recommended for CUDA builds).  
2. **Python Version**:  
   - Python 3.8 or later  
3. **CUDA (Optional, but recommended for speed)**:  
   - CUDA 11.x or later (to utilize GPU acceleration for PyTorch).  
   - NVIDIA drivers and CUDA toolkit properly installed.  
4. **Disk Space**:  
   - At least 5–10 GB free for models and dependencies.  

---

## Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/<your-username>/deepseek-multitask-app.git
   cd deepseek-multitask-app
   ```

2. **Create a Python Virtual Environment** (recommended)  
   ```bash
   python3 -m venv venv
   source venv/bin/activate       # On Windows: venv\Scripts\activate
   ```

3. **Upgrade `pip`**  
   ```bash
   pip install --upgrade pip
   ```

4. **Install Dependencies**  
   The `requirements.txt` should include:  
   ```text
   torch>=1.13.0
   transformers>=4.30.0
   gradio>=3.34.0
   deepseek-vl>=1.0.0
   ```
   Install with:  
   ```bash
   pip install -r requirements.txt
   ```

   > **Note:**  
   > - If you plan to run on GPU, ensure your `torch` installation matches your CUDA version. For example:  
   >   ```bash
   >   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   >   ```  
   >   Replace `cu118` with the appropriate CUDA version label (e.g., `cu117`, `cu113`).  
   > - `deepseek-vl` uses custom code; ensure `trust_remote_code=True` is allowed when loading the VL model.  

5. **Verify Installation**  
   Launch a Python REPL and try importing:  
   ```python
   >>> import torch
   >>> import gradio as gr
   >>> from transformers import AutoModelForCausalLM, AutoTokenizer
   >>> from deepseek_vl.models import VLChatProcessor, MultiModalityCausalLM
   >>> from deepseek_vl.utils.io import load_pil_images
   >>> print("All imports succeeded!")
   ```

---

## Model Downloads & Configuration

When you first run the application, the following models will be automatically downloaded from Hugging Face:

1. **Code Generation Model**  
   - Model ID: `deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B`  
   - Purpose: Causal‐LM fine‐tuned for Python code generation  

2. **Visual‐Language Model (VL)**  
   - Model Path: `deepseek-ai/deepseek-vl-1.3b-chat`  
   - Purpose: Multimodal chat model that can “see” an image and generate a text description  

These downloads can take several hundred megabytes to a few gigabytes, depending on the model size. Make sure you have a stable internet connection during this step. By default, both are cached under `~/.cache/huggingface/hub/` (or `C:\Users\<User>\.cache\huggingface\hub\` on Windows).

If you need to force a particular cache directory or use a local copy, set the environment variable before running:

```bash
export TRANSFORMERS_CACHE=/path/to/your/cache
export HF_HOME=/path/to/your/hf/home
```

---

## Running the App

1. **Navigate to Project Root**  
   ```bash
   cd deepseek-multitask-app
   ```

2. **Launch the Application**  
   ```bash
   python app.py
   ```
   - By default, Gradio will launch on `http://127.0.0.1:7860` in your browser.  
   - If you’d like to share your app publicly (Gradio’s tunnel), run:  
     ```bash
     python app.py --share
     ```
     A public URL (e.g., `https://xyz.gradio.app`) will be generated.  

3. **Quit the App**  
   - Press `CTRL+C` in the terminal where `app.py` is running.  

---

## Usage Guidelines

After launching, you’ll see the Gradio interface with two main tabs:

### 1. Code Generation Tab

- **Title**: “Code Generation (DeepSeek-R1-Distill-Qwen-1.5B)”  
- **Description**: Brief instructions on transforming natural language requests into Python code.  

#### Components:

1. **Prompt Input (Textbox)**  
   - Label: `Code Request`  
   - Placeholder: e.g., _“Create a Python function to calculate factorial of a number”_  
   - Default Value: “Create a Python function to calculate Fibonacci sequence with O(n) time complexity”  
   - Allows up to four lines of text.  

2. **Generation Parameters Accordion**  
   - **Max Tokens (Slider)**  
     - Range: 100 to 2048 (default: 512)  
     - Controls the maximum number of tokens the model can generate.  
   - **Temperature (Slider)**  
     - Range: 0.1 to 1.0 (step 0.1, default: 0.6)  
     - Higher values → more random outputs; lower → more deterministic.  
   - **Top-p (Slider)**  
     - Range: 0.1 to 1.0 (step 0.1, default: 0.9)  
     - Nucleus sampling cutoff.  
   - **Top-k (Slider)**  
     - Range: 1 to 100 (step 1, default: 50)  
     - Restricts sampling to top‐k tokens.  

3. **“Generate Code” Button**  
   - Clicking triggers the `generate_code_snippet` function with the above inputs.  

4. **Generated Python Code (Textbox)**  
   - Displays the raw Python snippet returned by the model (no comments or extra tokens).  
   - Up to 20 lines tall.  

---
   
### 2. Image Description Tab

- **Title**: “Image Description (deepseek-vl-1.3b-chat)”  
- **Description**: Generate detailed descriptions from uploaded images.  

#### Components:

1. **Image Input (Upload / Clipboard)**  
   - Label: `Upload Image`  
   - Users can drag & drop, click to upload from local disk, or paste from clipboard.  
   - Output is a PIL image object.  

2. **Description Parameters Accordion**  
   - **Detail Level (Radio Buttons)**  
     - Options:  
       - `Concise`: Short, high‐level summary (1–2 sentences).  
       - `Detailed`: In‐depth description (default).  
       - `Extreme`: Exhaustive enumeration of every visible detail.  
   - **Max Tokens (Slider)**  
     - Range: 100 to 2048 (default: 512)  
   - **Temperature (Slider)**  
     - Range: 0.1 to 1.0 (step 0.1, default: 0.6)  
   - **Top-p (Slider)**  
     - Range: 0.1 to 1.0 (step 0.1, default: 0.9)  
   - **Top-k (Slider)**  
     - Range: 1 to 100 (step 1, default: 50)  

3. **“Describe Image” Button**  
   - Triggers the `generate_image_description` function.  

4. **Image Description (Textbox)**  
   - Shows the generated description as plain text.  
   - Up to 20 lines tall.  

---

## Examples
...
## License

This project is licensed under the MIT License.
