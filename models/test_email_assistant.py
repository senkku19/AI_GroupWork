from LLMModel import LLMModel

# EMAIL_ASSISTANT_DIR = "../AI_GroupWork/models/local_openllama"

#EMAIL_ASSISTANT_DIR = "email_assistant"
EMAIL_ASSISTANT_DIR = "../AI_GroupWork\models\email_assistant"
# Config


# 1. Load model, change between email assistant and base model here by commenting
model = LLMModel(EMAIL_ASSISTANT_DIR)
#model = LLMModel(BASE_MODEL_DIR)  # Voit testata myös pelkällä basemallilla

# 2. Test email. This is the same format that was used in teaching!
sender = "jane@post.fi"
subject = "Service proposal"
body = """Hi!

I hope this message finds you well. I am reaching out to propose a new service that I believe could greatly benefit your company.

Best Regards,
Matti Meikäläinen"""

print("\n" + "="*40)
print(f"📧 TESTATAAN SÄHKÖPOSTIA:\nLähettäjä: {sender}\nAihe: {subject}\n")
print("="*40)

# 3. Run tasks by calling model methods

print("🔹 LUOKITTELU (Kategoria):")

category = model.classifyWork(sender, subject, body)
print(f"{category}")

print("\n🔹 KIIREELLISYYS:")
urgency = model.classifyUrgency(sender, subject, body)
print(f"{urgency}")

print("\n🔹 TIIVISTELMÄ:")
summary = model.createSummary(sender, subject, body)
print(f"{summary}")

print("\n🔹 VASTAUSEHDOTUS (Myönteinen):")
pos_reply = model.createAnswer(True, sender, subject, body)
print(f"{pos_reply}")

print("\n🔹 VASTAUSEHDOTUS (Kielteinen):")
neg_reply = model.createAnswer(False, sender, subject, body)
print(f"{neg_reply}")