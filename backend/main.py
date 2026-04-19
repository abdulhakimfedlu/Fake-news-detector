









from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Download NLTK data
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

app = FastAPI(title="Fake News Detector API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load BOTH models and vectorizer (for live comparison)
dt_model = joblib.load('dt_model.pkl')  # Decision Tree
rf_model = joblib.load('rf_model.pkl')  # Random Forest
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
    
    if len(cleaned.split()) < 20:
        return {
            "prediction": "Uncertain",
            "confidence": 0.0,
            "explanation": "Input too short—add more text for accurate detection.",
            "comparison": {
                "decision_tree": {"prediction": "N/A", "confidence": 0},
                "random_forest": {"prediction": "N/A", "confidence": 0}
            },
            "best_algorithm": "N/A"
        }
    
    vec = vectorizer.transform([cleaned])
    
    # Run BOTH models
    dt_pred = dt_model.predict(vec)[0]
    dt_probs = dt_model.predict_proba(vec)[0]
    dt_label = 'Fake' if dt_pred == 0 else 'Real'
    dt_conf = float(max(dt_probs)) * 100
    
    rf_pred = rf_model.predict(vec)[0]
    rf_probs = rf_model.predict_proba(vec)[0]
    rf_label = 'Fake' if rf_pred == 0 else 'Real'
    rf_conf = float(max(rf_probs)) * 100
    
    # Determine best (higher confidence or RF by default)
    best_algo = "Random Forest" if rf_conf > dt_conf else "Decision Tree"
    best_pred = rf_label if best_algo == "Random Forest" else dt_label
    best_conf = rf_conf if best_algo == "Random Forest" else dt_conf
    
    return {
        "prediction": best_pred,  # Overall prediction (from best)
        "confidence": round(best_conf, 1),
        "explanation": f"Comparison: Decision Tree says {dt_label} ({round(dt_conf, 1)}%), Random Forest says {rf_label} ({round(rf_conf, 1)}%). Best: {best_algo}.",
        "comparison": {
            "decision_tree": {"prediction": dt_label, "confidence": round(dt_conf, 1)},
            "random_forest": {"prediction": rf_label, "confidence": round(rf_conf, 1)}
        },
        "best_algorithm": best_algo
    }

@app.get("/")
def root():
    return {"message": "Fake News Detector API is running! Visit /docs for testing."}
