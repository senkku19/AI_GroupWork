from LLMModel import LLMModel
import os

# ----------------------
# KONFIGURAATIO
# ----------------------
# HUOM: Varmista, että tämä polku on sama, jossa alkuperäinen mallisi sijaitsee.
# Ensimmäisessä viestissäsi se oli "./local_openllama"
BASE_MODEL_DIR = "./local_openllama" 

# Tarkistetaan että polku on olemassa
if not os.path.exists(BASE_MODEL_DIR):
    print(f"VIRHE: Polkua {BASE_MODEL_DIR} ei löydy!")
    print("Varmista, että BASE_MODEL_DIR osoittaa kansioon, jossa OpenLLaMA-mallisi on.")
    exit()

print(f"🚀 Ladataan BASEMALLIA (ei hienosäätöä) polusta: {BASE_MODEL_DIR}")

# 1. Ladataan perusmalli
# LLMModel osaa käsitellä tilanteen, jossa adaptereita ei löydy -> se käyttää raakamallia.
model = LLMModel(BASE_MODEL_DIR)

# 2. Testidata (Sama kuin aiemmin)
sender = "rekrytointi@postipate.fi"
subject = "Tarjouspyyntö uudesta projektista"
body = """Moro!
Kiitos hyvästä työpajasta viime viikolla! 
Keskustelimme alustavasti uudesta projektista, ja haluaisin pyytää teiltä tarjouksen seuraavista palveluista:
- Verkkosivuston suunnittelu ja kehitys
- Sisällöntuotanto ja käännökset
- Hakukoneoptimointi (SEO)
Toivoisimme vastausta ensi viikkoon mennessä, jotta ehdimme aikatauluun.

Ystävällisin terveisin,
Matti Meikäläinen"""

print("\n" + "="*40)
print(f"📧 TESTATAAN BASEMALLIA SÄHKÖPOSTILLA:\nLähettäjä: {sender}\nAihe: {subject}\n")
print("="*40)

# 3. Ajetaan samat testit

print("🔹 LUOKITTELU (Kategoria):")
category = model.classifyWork(sender, subject, body)
print(f"   -> {category}")

print("\n🔹 KIIREELLISYYS:")
urgency = model.classifyUrgency(sender, subject, body)
print(f"   -> {urgency}")

print("\n🔹 TIIVISTELMÄ:")
summary = model.createSummary(sender, subject, body)
print(f"   -> {summary}")

print("\n🔹 VASTAUSEHDOTUS (Myönteinen):")
pos_reply = model.createAnswer(True, sender, subject, body)
print(f"{pos_reply}")

print("\n🔹 VASTAUSEHDOTUS (Kielteinen):")
neg_reply = model.createAnswer(False, sender, subject, body)
print(f"{neg_reply}")