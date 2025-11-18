import os
import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, BitsAndBytesConfig, TrainerCallback
from datasets import Dataset
from peft import LoraConfig, get_peft_model, TaskType
from tqdm import tqdm

# ----------------------
# CONFIG
# ----------------------
BASE_MODEL_DIR = "./local_openllama"
OUTPUT_DIR = "./email_assistant"

TRAIN_CSV = "AI_GroupWork/data/emails_train.csv"
VAL_CSV = "AI_GroupWork/data/emails_val.csv"

MAX_LENGTH = 512
BATCH_SIZE = 2
EPOCHS = 2
LEARNING_RATE = 2e-4

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# ----------------------
# Load base model/tokenizer
# ----------------------
print("🔹 Loading Finnish base model...")
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_DIR, use_fast=False)
quant_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16, bnb_4bit_use_double_quant=True)

base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL_DIR,
    quantization_config=quant_config,
    device_map="auto"
)

# ----------------------
# Prepare datasets
# ----------------------
def load_csv_dataset(path):
    df = pd.read_csv(path)
    def make_prompt(row):
        return f"""Sähköposti:
Lähettäjä: {row['sender']}
Aihe: {row['subject']}
Viesti: {row['body']}

Tehtävä:
- Kategoria: {row['category']}
- Kiireellisyys: {row['urgency']}
- Tiivistelmä: {row['summary']}
- Myönteinen vastaus: {row['positive_reply']}
- Kielteinen vastaus: {row['negative_reply']}
"""
    df["text"] = df.apply(make_prompt, axis=1)
    return Dataset.from_pandas(df[["text"]])

train_dataset = load_csv_dataset(TRAIN_CSV)
val_dataset = load_csv_dataset(VAL_CSV)

def tokenize(batch):
    enc = tokenizer(batch["text"], truncation=True, padding="max_length", max_length=MAX_LENGTH)
    enc["labels"] = enc["input_ids"].copy()
    return enc

train_dataset = train_dataset.map(tokenize, batched=True)
val_dataset = val_dataset.map(tokenize, batched=True)

# ----------------------
# LoRA config
# ----------------------
lora_config = LoraConfig(
    r=8, lora_alpha=32,
    target_modules=["q_proj","v_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

model = get_peft_model(base_model, lora_config)
model.to(device)

# ----------------------
# Callback for metrics
# ----------------------
class MetricsCallback(TrainerCallback):
    def __init__(self):
        self.logs = []

    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs and "loss" in logs:
            self.logs.append({"step": state.global_step, "epoch": state.epoch, "loss": logs["loss"]})
        if logs and "eval_loss" in logs:
            self.logs.append({"step": state.global_step, "epoch": state.epoch, "eval_loss": logs["eval_loss"]})

callback = MetricsCallback()

# ----------------------
# TrainingArguments & Trainer
# ----------------------
training_args = TrainingArguments(
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=1,
    num_train_epochs=EPOCHS,
    learning_rate=LEARNING_RATE,
    logging_steps=5,
    save_strategy="epoch",
    output_dir=OUTPUT_DIR,
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer,
    callbacks=[callback]
)

# ----------------------
# Training loop with tqdm
# ----------------------
print("🔹 Starting training...")
trainer.train()

# ----------------------
# Save model + metrics
# ----------------------
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

pd.DataFrame(callback.logs).to_csv(os.path.join(OUTPUT_DIR, "metrics.csv"), index=False)

print("✅ Email assistant saved to", OUTPUT_DIR)
print("📊 Metrics saved to metrics.csv")
