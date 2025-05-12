from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import torch

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment"

# Load tokenizer and model (with optional local cache)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir="./model_cache")
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, cache_dir="./model_cache")

# Use GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

labels = ["negative", "neutral", "positive"]

def predict_text(text: str):
    encoded_input = tokenizer(text, return_tensors='pt', truncation=True).to(device)
    
    with torch.no_grad():
        output = model(**encoded_input)

    scores = softmax(output.logits[0].cpu().numpy())
    prediction = labels[scores.argmax()]

    # Map sentiment to risk levels
    if scores[0] > 0.7:
        risk = "High"
    elif scores[1] > 0.5:
        risk = "Moderate"
    else:
        risk = "Low"
    
    return {
        "prediction": prediction,
        "scores": dict(zip(labels, map(float, scores))),
        "risk": risk
    }

# For test
if __name__ == "__main__":
    print(predict_text("not good"))
