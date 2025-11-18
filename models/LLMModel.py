import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

class LLMModel:
    def __init__(self, model_path):
        print("🔹 Loading tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        print("🔹 Loading model...")
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map="auto",
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True
        )

        # Load PEFT/LoRA weights if present
        try:
            self.model = PeftModel.from_pretrained(self.model, model_path)
        except:
            pass

        self.model.eval()
        print("✅ Model ready.")

    def _generate(self, prompt, max_new_tokens=200):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        output = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.2,
            top_p=0.9,
            eos_token_id=self.tokenizer.eos_token_id
        )
        return self.tokenizer.decode(output[0], skip_special_tokens=True).strip()

    def classifyWork(self, inputText):
        prompt = f"""Classify the following email into work-related or leisure-related.
Possible classes: "Work", "Leisure".

Teksti:
{inputText}

Answer only with one word:
"""
        return self._generate(prompt, max_new_tokens=10)

    def classifyUrgency(self, inputText):
        prompt = f"""Classify the urgency of following email.
Possible classes: "Low", "Medium", "High".

Teksti:
{inputText}

Answer only with one word:
"""
        return self._generate(prompt, max_new_tokens=10)

    def createSummary(self, inputText):
        prompt = f"""Create a brief summary of the following email:

{inputText}

Summary:
"""
        return self._generate(prompt, max_new_tokens=120)

    def createAnswer(self, positiveAnswer, inputText):
        instruction = "Kirjoita kohtelias ja positive vastaus." if positiveAnswer else "Kirjoita kohtelias mutta negative vastaus."
        prompt = f"""{instruction}

Sähköposti:
{inputText}

Vastaus:
"""
        return self._generate(prompt, max_new_tokens=200)
