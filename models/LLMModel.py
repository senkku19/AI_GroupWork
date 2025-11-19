import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

class LLMModel:
    def __init__(self, model_path):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"🔹 Loading tokenizer from {model_path}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        print(f"🔹 Loading base model & LoRA adapters on {self.device}...")
        
        # Ladataan perusmalli
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map="auto",
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True
        )
        
        # Ladataan LoRA-adapterit
        try:
            self.model = PeftModel.from_pretrained(self.model, model_path)
        except:
            print("Info: Model loaded directly (merged or base model).")

        self.model.eval()
        print("✅ Model ready.")

    def _format_email_prompt(self, sender, subject, body, target_field):
        """
        Rakentaa opetusdataa vastaavan rakenteen erillisistä kentistä.
        """
        # Käytetään oletusarvoja, jos kentät ovat tyhjiä
        sender = sender if sender else "Tuntematon"
        subject = subject if subject else "Ei aihetta"
        body = body if body else ""

        # Rakenne vastaa tarkasti make_prompt -funktiota koulutuksessa
        prompt = f"""Sähköposti:
Lähettäjä: {sender}
Aihe: {subject}
Viesti: {body}

Tehtävä:
- {target_field}:"""
        return prompt

    def _generate(self, prompt, max_new_tokens=100, stop_at_newline=True):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=0.2,
                top_p=0.9,
                eos_token_id=self.tokenizer.eos_token_id,
                pad_token_id=self.tokenizer.eos_token_id,
                repetition_penalty=1.1 
            )
        
        full_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        generated_text = full_text[len(prompt):].strip()
        
        if stop_at_newline:
            generated_text = generated_text.split('\n')[0].strip()
            
        return generated_text

    # --- PUBLIC INTERFACE ---

    def classifyWork(self, sender, subject, body):
        prompt = self._format_email_prompt(sender, subject, body, "Kategoria")
        return self._generate(prompt, max_new_tokens=10, stop_at_newline=True)

    def classifyUrgency(self, sender, subject, body):
        prompt = self._format_email_prompt(sender, subject, body, "Kiireellisyys")
        return self._generate(prompt, max_new_tokens=10, stop_at_newline=True)

    def createSummary(self, sender, subject, body):
        prompt = self._format_email_prompt(sender, subject, body, "Tiivistelmä")
        return self._generate(prompt, max_new_tokens=150, stop_at_newline=True)

    def createAnswer(self, positiveAnswer, sender, subject, body):
        field = "Myönteinen vastaus" if positiveAnswer else "Kielteinen vastaus"
        prompt = self._format_email_prompt(sender, subject, body, field)
        
        raw_answer = self._generate(prompt, max_new_tokens=200, stop_at_newline=False)
        
        # Siivotaan, jos malli alkaa generoida seuraavaa kenttää
        if "\n-" in raw_answer:
            raw_answer = raw_answer.split("\n-")[0]
            
        return raw_answer.strip()