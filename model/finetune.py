# llama3b_finetune_pipeline.py

import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from datasets import load_dataset, load_from_disk
from peft import LoraConfig, get_peft_model, TaskType
from tqdm import tqdm
import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
MODEL_NAME = "openlm-research/open_llama_3b_v2"

DATA_PATH = "AI_GroupWork/data/movie-subtitles-finnish.txt"
TOKENIZED_PATH = "./tokenized_dataset"
MODEL_LOCAL_DIR = "./local_model"
OUTPUT_DIR = "./llama3b-finetuned"

MAX_LENGTH = 512
BATCH_SIZE = 2
EPOCHS = 1  # Pieni luku testiin
LEARNING_RATE = 2e-4

device = "cuda" if torch.cuda.is_available() else "cpu"

# -----------------------------
# Tokenizer & Model (lataus/tallennus)
# -----------------------------
if os.path.exists(MODEL_LOCAL_DIR):
    print("🔹 Ladataan tokenizer ja malli levyltä...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_LOCAL_DIR, use_fast=False)
    base_model = AutoModelForCausalLM.from_pretrained(
        MODEL_LOCAL_DIR,
        device_map="auto",
        load_in_4bit=True
    )
else:
    print("🔹 Ladataan tokenizer ja malli HuggingFacesta...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    base_model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="auto",
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.float16
    )
    os.makedirs(MODEL_LOCAL_DIR, exist_ok=True)
    tokenizer.save_pretrained(MODEL_LOCAL_DIR)
    base_model.save_pretrained(MODEL_LOCAL_DIR)

# -----------------------------
# Dataset
# -----------------------------
if os.path.exists(TOKENIZED_PATH):
    print("🔹 Ladataan tokenisoitu dataset levyltä...")
    tokenized_dataset = load_from_disk(TOKENIZED_PATH)
else:
    print("🔹 Tokenisoidaan dataset...")
    dataset = load_dataset("text", data_files={"train": DATA_PATH})

    def tokenize(batch):
        return tokenizer(batch["text"], padding="max_length", truncation=True, max_length=MAX_LENGTH)

    tokenized_dataset = dataset.map(tokenize, batched=True)
    tokenized_dataset.save_to_disk(TOKENIZED_PATH)

# -----------------------------
# QLoRA (LoRA) konfiguraatio
# -----------------------------
lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

model = get_peft_model(base_model, lora_config)
model.to(device)

# -----------------------------
# Training
# -----------------------------
training_args = TrainingArguments(
    per_device_train_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=1,
    warmup_steps=10,
    num_train_epochs=EPOCHS,
    learning_rate=LEARNING_RATE,
    logging_steps=5,
    output_dir=OUTPUT_DIR,
    save_strategy="epoch",
    report_to="none"
)

metrics_history = []

def compute_metrics(eval_pred):
    return {}

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

print("🔹 Starting training...")
for epoch in range(EPOCHS):
    for step, _ in enumerate(tqdm(tokenized_dataset["train"], desc=f"Epoch {epoch+1}/{EPOCHS}")):
        trainer.train()
        metrics_history.append({
            "epoch": epoch + 1,
            "step": step + 1,
            "loss": trainer.state.log_history[-1]["loss"] if trainer.state.log_history else None
        })

# -----------------------------
# Metrics ja tallennus
# -----------------------------
os.makedirs(OUTPUT_DIR, exist_ok=True)
pd.DataFrame(metrics_history).to_csv(os.path.join(OUTPUT_DIR, "metrics.csv"), index=False)

model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
print(f"✅ Model saved to {OUTPUT_DIR}")

# -----------------------------
# Sovellusfunktiot
# -----------------------------
def createAnswer(positiveAnswer: str, inputText: str):
    prompt = f"{inputText}\nVastaus:\n{positiveAnswer}"
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    output = model.generate(**inputs, max_length=MAX_LENGTH)
    return tokenizer.decode(output[0], skip_special_tokens=True)

def summarizeEmail(inputText: str):
    prompt = f"Tiivistä seuraava sähköposti:\n{inputText}\nTiivistelmä:"
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    output = model.generate(**inputs, max_length=MAX_LENGTH)
    return tokenizer.decode(output[0], skip_special_tokens=True)

def classifyEmail(inputText: str):
    prompt = f"Luokittele seuraava sähköposti työhön tai vapaa-aikaan, ja arvioi kiireellisyys:\n{inputText}\nLuokitus:"
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    output = model.generate(**inputs, max_length=MAX_LENGTH)
    return tokenizer.decode(output[0], skip_special_tokens=True)

print("🔹 Pipeline valmis! Voit nyt käyttää createAnswer(), summarizeEmail(), classifyEmail()")
