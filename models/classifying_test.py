import pandas as pd
from LLMModel import LLMModel
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import seaborn as sns
import matplotlib.pyplot as plt

# Configuration
TEST_CSV = "../AI_GroupWork/data/emails_english_val.csv"

VALID_CATEGORIES = ["business", "pleasure"]
VALID_URGENCIES = ["1", "2", "3"]

# Load model
MODEL_DIR = "../AI_GroupWork/models/email_assistant"
# MODEL_DIR = "../AI_GroupWork/models/local_openllama" # Test base model 
model = LLMModel(MODEL_DIR)

# Load test data
df = pd.read_csv(TEST_CSV)
emails = df.to_dict(orient="records")

# Collect predictions
y_true_category = []
y_pred_category = []

y_true_urgency = []
y_pred_urgency = []

for email in emails:
    sender = email.get("sender", "")
    subject = email.get("subject", "")
    body = email.get("body", "")

    # Category
    true_cat = email.get("category", "").strip()
    pred_cat = model.classifyWork(sender, subject, body).strip()
    y_true_category.append(true_cat)
    y_pred_category.append(pred_cat)

    # Urgency
    true_urg = str(email.get("urgency", "")).strip()
    pred_urg = model.classifyUrgency(sender, subject, body).strip()
    y_true_urgency.append(true_urg)
    y_pred_urgency.append(pred_urg)

# Filter only valid classes
filtered_indices_cat = [i for i, c in enumerate(y_true_category) if c in VALID_CATEGORIES]
y_true_category = [y_true_category[i] for i in filtered_indices_cat]
y_pred_category = [y_pred_category[i] for i in filtered_indices_cat]

filtered_indices_urg = [i for i, u in enumerate(y_true_urgency) if u in VALID_URGENCIES]
y_true_urgency = [y_true_urgency[i] for i in filtered_indices_urg]
y_pred_urgency = [y_pred_urgency[i] for i in filtered_indices_urg]

# Print classification reports
print("=== CATEGORY ===")
print(classification_report(y_true_category, y_pred_category, labels=VALID_CATEGORIES, zero_division=0))
print(f"Accuracy: {accuracy_score(y_true_category, y_pred_category):.3f}\n")

print("=== URGENCY ===")
print(classification_report(y_true_urgency, y_pred_urgency, labels=VALID_URGENCIES, zero_division=0))
print(f"Accuracy: {accuracy_score(y_true_urgency, y_pred_urgency):.3f}\n")

# Plot confusion matrices
def plot_confusion(y_true, y_pred, labels, title, filename):
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    plt.figure(figsize=(6,5))
    sns.heatmap(cm, annot=True, fmt="d", xticklabels=labels, yticklabels=labels, cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()

plot_confusion(y_true_category, y_pred_category, VALID_CATEGORIES, "Category Confusion Matrix", "category_confusion_matrix.png")
plot_confusion(y_true_urgency, y_pred_urgency, VALID_URGENCIES, "Urgency Confusion Matrix", "urgency_confusion_matrix.png")
