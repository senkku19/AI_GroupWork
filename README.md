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
- **Python 3.10.19 or later**
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

Make sure your **Outlook** is open, then run:

```bash
python main.py
```
