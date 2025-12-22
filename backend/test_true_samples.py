import pandas as pd
import joblib
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

def clean_text(text):
    if pd.isna(text):
        return ""
    text = re.sub(r'[^a-zA-Z\s]', '', str(text).lower())
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if w not in stop_words and len(w) > 2]
    return ' '.join(tokens)

# Load model & vectorizer
model = joblib.load('best_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Load True.csv & pick 3 samples (rows 0, 100, 200 for variety)
true_df = pd.read_csv('data/True.csv')
samples = true_df.iloc[[0, 100, 200]]  # Sample rows

for idx, row in samples.iterrows():
    content = str(row['title']) + ' ' + str(row['text'])  # Full content
    cleaned = clean_text(content)
    vec = vectorizer.transform([cleaned])
    pred = model.predict(vec)[0]
    probs = model.predict_proba(vec)[0]
    label = 'Fake' if pred == 0 else 'Real'
    confidence = max(probs) * 100
    print(f"Sample {idx}: {label} ({confidence:.1f}% confidence)")
    print(f"Title: {row['title'][:100]}...")  # Short title preview
    print(f"Cleaned length: {len(cleaned.split())} words")  # Check if full
    print("---")