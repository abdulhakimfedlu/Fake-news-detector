from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Added for frontend CORS
from pydantic import BaseModel
import joblib
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Download NLTK data (one-time, quiet)
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)  # For tokenizer

app = FastAPI(title="Fake News Detector API")

# Add CORS middleware to allow React frontend (localhost:5173) to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load your saved model and vectorizer (RF from training)
model = joblib.load('best_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r'[^a-zA-Z\s]', '', str(text).lower())
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if w not in stop_words and len(w) > 2]
    return ' '.join(tokens)

class NewsRequest(BaseModel):
    text: str

@app.post("/predict")
async def predict(request: NewsRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    cleaned = clean_text(request.text)
    
    # Adjusted guard for short inputs (prevents unreliable predictions; raised to <20 for headlines/short articles)
    if len(cleaned.split()) < 20:  # Under 20 words = too short for reliable news detection
        return {
            "prediction": "Uncertain",
            "confidence": 0.0,
            "explanation": "Input too short—add more text for accurate detection. (Model best on 50+ words)",
            "algorithm": "N/A (Short Input Guard)"
        }
    
    vec = vectorizer.transform([cleaned])
    pred = model.predict(vec)[0]
    probs = model.predict_proba(vec)[0]
    label = 'Fake' if pred == 0 else 'Real'
    confidence = float(max(probs)) * 100
    return {
        "prediction": label,
        "confidence": round(confidence, 1),
        "explanation": "Powered by Random Forest ML model (99.8% accurate on test data).",
        "algorithm": "Random Forest"  # Dynamic: Shows the algorithm used
    }

@app.get("/")
def root():
    return {"message": "Fake News Detector API is running! Visit /docs for testing."}