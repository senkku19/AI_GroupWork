# train_finnish_basic.py

import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from transformers import BitsAndBytesConfig, TrainerCallback
from datasets import load_dataset, load_from_disk
from peft import LoraConfig, get_peft_model, TaskType
from tqdm import tqdm
import pandas as pd

# ------------------------------------
# CONFIG
# ------------------------------------
MODEL_NAME = "openlm-research/open_llama_3b_v2"
DATA_PATH = "AI_GroupWork/data/movie-subtitles-finnish_smallest.txt"
TOKENIZED_PATH = "./tokenized_finnish_basic"
MODEL_LOCAL_DIR = "./local_openllama"
OUTPUT_DIR = "./finnish_basic"

MAX_LENGTH = 512
BATCH_SIZE = 2
EPOCHS = 1
LEARNING_RATE = 2e-4

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

max_memory = {0: "7GB", "cpu": "30GB"}


# ------------------------------------
# FLASH ATTENTION ENABLE
# ------------------------------------
def enable_flash_attention(model):
    """
    Yrittää ottaa käyttöön FlashAttention2 → jos ei onnistu → SDPA → fallback Eager.
    """
    try:
        model = model.to(memory_format=torch.contiguous_format)
        model.config.attn_implementation = "flash_attention_2"
        print("🔹 FlashAttention 2 enabled")
    except Exception as e1:
        print(f"⚠️ FlashAttention2 unavailable ({e1}), trying SDPA...")
        try:
            model.config.attn_implementation = "sdpa"
            print("🔹 SDPA attention enabled")
        except Exception as e2:
            print(f"⚠️ SDPA failed ({e2}), falling back to Eager.")
            model.config.attn_implementation = "eager"

    return model


# ------------------------------------
# LOAD TOKENIZER + MODEL
# ------------------------------------
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

if os.path.exists(MODEL_LOCAL_DIR):
    print("🔹 Loading tokenizer + model from disk...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_LOCAL_DIR, use_fast=False)
    base_model = AutoModelForCausalLM.from_pretrained(
        MODEL_LOCAL_DIR,
        quantization_config=quant_config,
        device_map="auto",
        max_memory=max_memory
    )
else:
    print("🔹 Loading from HuggingFace...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    base_model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=quant_config,
        device_map="auto",
        max_memory=max_memory
    )

    os.makedirs(MODEL_LOCAL_DIR, exist_ok=True)
    tokenizer.save_pretrained(MODEL_LOCAL_DIR)
    base_model.save_pretrained(MODEL_LOCAL_DIR)

# Enable FlashAttention2
base_model = enable_flash_attention(base_model)


# ------------------------------------
# DATASET + SEQUENCE PACKING (FIXED)
# ------------------------------------
if os.path.exists(TOKENIZED_PATH):
    print("🔹 Loading packed dataset...")
    tokenized_dataset = load_from_disk(TOKENIZED_PATH)

else:
    print("🔹 Loading raw dataset...")
    raw_dataset = load_dataset("text", data_files={"train": DATA_PATH})

    # --- Stage 1: tokenize without padding ---
    def tokenize(batch):
        return tokenizer(
            batch["text"],
            truncation=True,
            max_length=MAX_LENGTH,
            add_special_tokens=False      # IMPORTANT
        )

    print("🔹 Tokenizing dataset...")
    tokenized = raw_dataset.map(
        tokenize,
        batched=True,
        batch_size=1000,
        remove_columns=["text"],
        desc="Tokenizing"
    )

    # --- Stage 2: pack sequences (concatenate + chunk) ---
    def pack(examples):
        # Flatten all token lists
        all_tokens = []
        for seq in examples["input_ids"]:
            all_tokens.extend(seq)

        # Make fixed-size chunks
        chunk_size = MAX_LENGTH
        chunks = [
            all_tokens[i:i + chunk_size]
            for i in range(0, len(all_tokens), chunk_size)
            if len(all_tokens[i:i + chunk_size]) == chunk_size
        ]

        return {
            "input_ids": chunks,
            "labels": chunks
        }

    print("🔹 Packing sequences (concat + 512)...")
    packed = tokenized.map(
        pack,
        batched=True,
        remove_columns=tokenized["train"].column_names,
        desc="Packing"
    )

    tokenized_dataset = packed
    tokenized_dataset.save_to_disk(TOKENIZED_PATH)

# ------------------------------------
# LoRA CONFIG
# ------------------------------------
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


# ------------------------------------
# LOSS TRACKER
# ------------------------------------
class LossTrackerCallback(TrainerCallback):
    def __init__(self):
        self.history = []

    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs and "loss" in logs:
            self.history.append({
                "step": state.global_step,
                "epoch": state.epoch,
                "loss": logs["loss"]
            })


loss_callback = LossTrackerCallback()


# ------------------------------------
# TRAINING
# ------------------------------------
training_args = TrainingArguments(
    per_device_train_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=1,
    warmup_steps=5,
    num_train_epochs=EPOCHS,
    learning_rate=LEARNING_RATE,
    logging_steps=5,
    output_dir=OUTPUT_DIR,
    save_strategy="epoch",
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    tokenizer=tokenizer,
    callbacks=[loss_callback]
)

print("🔹 Starting training...")
trainer.train()


# ------------------------------------
# SAVE MODEL + METRICS
# ------------------------------------
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

pd.DataFrame(loss_callback.history).to_csv(
    os.path.join(OUTPUT_DIR, "metrics.csv"),
    index=False
)

print("✅ Finnish basic model saved")
print("📊 Loss history saved to metrics.csv")