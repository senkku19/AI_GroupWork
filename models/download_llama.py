# download_openllama.py
# Downloads the OpenLLaMA 3B v2 model with 4-bit quantization and saves it locally.
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import BitsAndBytesConfig


MODEL_NAME = "openlm-research/open_llama_3b_v2"
MODEL_LOCAL_DIR = "./local_openllama"

max_memory = {0: "7GB", "cpu": "30GB"} # Change to your device, this works with 8GB VRAM GPU

# Quantization (4-bit)
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

# Download model if not exists
if os.path.exists(MODEL_LOCAL_DIR):
    print("Local model already exists.")
else:
    print(f"Downloading model: {MODEL_NAME}")
    os.makedirs(MODEL_LOCAL_DIR, exist_ok=True)

    # Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Model
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=quant_config,
        device_map="auto",
        max_memory=max_memory
    )

    print("Saving model to local directory...")
    tokenizer.save_pretrained(MODEL_LOCAL_DIR)
    model.save_pretrained(MODEL_LOCAL_DIR)

    print(f"Model saved to {MODEL_LOCAL_DIR}")

print("Done.")
