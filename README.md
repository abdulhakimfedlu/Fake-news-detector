# 🕵️‍♂️ AI-Powered Fake News Detector

> *"In an era of information overload, truth is the most valuable currency."*

A comprehensive full-stack machine learning application designed to combat misinformation. This system analyzes news articles in real-time, leveraging advanced Natural Language Processing (NLP) and ensemble learning techniques to determine credibility with high precision.

---

## 🌍 Why Machine Learning for Fake News?

The rapid spread of misinformation on social media and digital platforms poses a significant threat to public discourse. Manual verification is no longer scalable against the volume of content generated daily.

**Machine Learning offers a scalable solution by:**
- **Pattern Recognition**: Identifying subtle linguistic cues and writing styles often associated with deceptive content.
- **Speed & Scale**: Processing thousands of articles in seconds, a task impossible for human fact-checkers.
- **Unbiased Analysis**: Providing data-driven probability scores, reducing human subjectivity.

---

## 🧠 Algorithms & Model Selection

This project utilizes a **Dual-Model Architecture** to ensure robust and explainable predictions. We chose these specific algorithms to balance accuracy with interpretability.

### 1. Random Forest Classifier 🌳🌳
**Why we chose it:**
Random Forest is an ensemble learning method that constructs a multitude of decision trees at training time.
- **High Accuracy**: By averaging the results of many trees, it minimizes the risk of overfitting (memorizing the data) that single trees suffer from.
- **Robustness**: It handles high-dimensional text data effectively, ensuring reliability across diverse topics.

### 2. Decision Tree Classifier 🌲
**Why we chose it:**
- **Explainability**: Unlike "black box" deep learning models, Decision Trees mimic human decision-making logic. This allows us to trace *why* a specific article was flagged, making the AI's decision transparent.
- **Speed**: Extremely fast inference times make it ideal for real-time applications.

### 🤖 The "Hybrid" Approach
Our system runs **both models simultaneously** for every query. It compares their confidence scores and presents the user with the most reliable prediction, offering a "second opinion" automatically.

---

## ⚡ Key Features

### User-Facing Application
- **Real-Time Classification**: Instant analysis of text input with immediate "Real" or "Fake" verdicts.
- **Confidence Scoring**: Transparent probability percentage (e.g., "98.5% Confidence") to gauge certainty.
- **Multi-Model Insight**: View comparative results from both the Decision Tree and Random Forest models side-by-side.
- **Responsive Design**: A modern, mobile-first interface built with **React** and **Tailwind CSS**, ensuring accessibility on all devices.

### Development & Admin Features
- **RESTful API**: A high-performance backend built with **FastAPI** for seamless integration.
- **Extensible ML Pipeline**: Modular Python codebase using **scikit-learn** and **NLTK**, making it easy to retrain models or add new algorithms.
- **Clean Architecture**: Separation of concerns between the frontend (UI), backend (API), and model (Data Science).

---

## 🛠️ Tech Stack

### Backend (Python 🐍)
- **FastAPI**: For building a high-speed, modern web API.
- **Scikit-learn**: For implementing the Machine Learning algorithms.
- **NLTK (Natural Language Toolkit)**: For advanced text processing (tokenization, stopword removal).
- **Pandas & NumPy**: For efficient data manipulation.

### Frontend (Modern Web ⚛️)
- **React (Vite)**: For a fast, interactive user interface.
- **Tailwind CSS**: For professional, responsive styling.
- **Axios/Fetch**: For asynchronous API communication.

---

## 🚀 Installation & Setup

Follow these steps to deploy the application locally.

### Prerequisites
- Python 3.8+
- Node.js & npm
- Git

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd AI-Assignment
```

### 2. Backend Setup
```bash
cd backend
# Create a virtual environment (optional but recommended)
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn main:app --reload
```
*The server will start at `http://localhost:8000`*

### 3. Frontend Setup
```bash
cd frontend/Fareal

# Install Node modules
npm install

# Start the development server
npm run dev
```
*The application will open at `http://localhost:5173`*

---

## 🔬 Model Training Workflow

To update the AI with new data:
1.  Add your dataset (CSV) to `backend/data/`.
2.  Run the training script:
    ```bash
    python backend/train_model.py
    ```
3.  The system will automatically generate new `.pkl` files and save usage metrics.
