# AI_GroupWork

## Project Overview

This project implements an AI-powered assistant for Outlook email.  
The system reads incoming emails, analyzes their content, and provides helpful automated features such as:

- **Business / pleasure classification**
- **Urgency rating (1–3)**
- **Short summaries**
- **Positive and negative reply drafts**

Emails are retrieved through the Windows Outlook API, processed by a LLaMA-based language model, and shown in a graphical user interface for easy interaction.

The goal is to speed up email management and help users focus on what matters by providing clear insights and AI-assisted responses.

## Installation Guide

## Requirements

- **Python 3.10.19 (later versions might work but not tested)**
- **A virtual environment**
  > **Note:**  
  > The steps below use **Anaconda/Miniconda** as an example for creating a Python 3.10.19 environment.  
  > You may use any virtual-environment tool as long as the Python version matches.

## 1. Create and Activate a Virtual Environment (Conda Example)

Open **Anaconda Prompt** and run:

```bash
conda create -n ai_project python=3.10.19
conda activate ai_project
```

## 2. Install Dependencies

```bash
pip install features
pip install PyQt5
```

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

```bash
pip install --upgrade transformers bitsandbytes peft accelerate datasets trl
pip install SentencePiece
pip install protobuf
```

```bash
pip install pywin32
```

```bash
pip install tqdm pandas matplotlib
pip install beautifulsoup4
pip install futures
```

## 3. Select Python Interpreter

In your IDE (e.g., **VS Code**):

```
Python: Select Interpreter → Choose "ai_project"
```

## 4. Download Model Files

Run:

```bash
python download_llama.py
```

After the download completes:

- Move the downloaded **local_openllama** directory  
  inside the **models/** folder.

## 5. Run the Application

Make sure your **Outlook** application is running, then run:

```bash
python main.py
```

# Training and testing

This project used _train_email_assistant.py_ script to fine-tune Open LLaMa 3B v2 model.
Supervised fine-tuning (SFT) training is performed to LoRA adapter and the script uses 4-bit quantization for more feasible VRAM usage.

## Training new model

Email assistant -model was trained using RTX 3070ti GPU that supported CUDA and the code is optimised for that. Feel free to modify the code to match your devices capabilities.
Training results to trained LoRA that may be attached to base model. Training also saves loss per step data to **metrics.csv** file.

## Testing model performance

Model performance can be tested with **test_email_assistant.py** and **classifying_test**

Comment/ uncomment model directory paths to change between base model and trained model to compare models.

**test_email_assistant.py** enables testing with single email
**classifying_test** tests the model's classifying elements

For testing it is also required to install some packages:

```bash
pip install scikit-learn
pip install matplotlib
pip install seaborn
```

## Contributors:

- _Olli Hilke_ - [Oh-BugHit](https://github.com/OH-BugHit)
-
