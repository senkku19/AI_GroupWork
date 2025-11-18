from LLMModel import LLMModel

EMAIL_ASSISTANT_DIR = "./email_assistant"

# Load trained model
model = LLMModel(EMAIL_ASSISTANT_DIR)

# Test input
#test_email = """Hei, minulla on ongelma läppärin verkkoasetusten kanssa.
# En pääse yhdistämään VPN-yhteyteen ja tarvitsisin tukea mahdollisimman pian."""

test_email = """Hi! I got huge issue! Can you help me woth this LLM model training?"""



print("=== CLASSIFY WORK ===")
print(model.classifyWork(test_email))

print("\n=== CLASSIFY URGENCY ===")
print(model.classifyUrgency(test_email))

print("\n=== SUMMARY ===")
print(model.createSummary(test_email))

print("\n=== POSITIVE ANSWER ===")
print(model.createAnswer(True, test_email))

print("\n=== NEGATIVE ANSWER ===")
print(model.createAnswer(False, test_email))
