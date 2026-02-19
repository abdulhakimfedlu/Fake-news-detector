






import joblib
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

def clean_text(text):
    if not text: return ""
    text = re.sub(r'[^a-zA-Z\s]', '', str(text).lower())
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if w not in stop_words and len(w) > 2]
    return ' '.join(tokens)

# Load
model = joblib.load('best_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Test Prediction
test_text = "Breaking: Secret alien invasion plot exposed by whistleblower!"  # Fake-like
cleaned = clean_text(test_text)
vec = vectorizer.transform([cleaned])
pred = model.predict(vec)[0]
probs = model.predict_proba(vec)[0]
label = 'Fake' if pred == 0 else 'Real'
confidence = max(probs) * 100
print(f"Test Prediction: {label} (Confidence: {confidence:.1f}%)")
