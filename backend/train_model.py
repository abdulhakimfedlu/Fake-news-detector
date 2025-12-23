import pandas as pd  # For loading/handling data
import numpy as np   # For numbers
from sklearn.model_selection import train_test_split  # For splitting data
from sklearn.feature_extraction.text import TfidfVectorizer  # Text to numbers
from sklearn.tree import DecisionTreeClassifier  # Changed: Decision Tree instead of Logistic
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib  # To save model
import re  # For cleaning text
from nltk.corpus import stopwords  # Ignore common words
from nltk.tokenize import word_tokenize
import nltk
import matplotlib.pyplot as plt
import seaborn as sns

# Download NLTK data (one-time)
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)  # For modern tokenizer

# Step 1: Load Data
print("Loading data...")
fake = pd.read_csv('data/Fake.csv')  # Fake news
true = pd.read_csv('data/True.csv')  # Real news

# Add labels: 0 for fake, 1 for real
fake['label'] = 0
true['label'] = 1

# Combine
df = pd.concat([fake, true], ignore_index=True)

# Fix bias: Oversample reals to match fakes
fake_count = len(df[df['label'] == 0])
real_df = df[df['label'] == 1].sample(n=fake_count, replace=True, random_state=42)
fake_df = df[df['label'] == 0]
df = pd.concat([real_df, fake_df], ignore_index=True)
print("Balanced shape:", df.shape)
print("Balance:\n", df['label'].value_counts())

print("Dataset Shape:", df.shape)  # ~46K rows after balancing
print("Fake/Real Balance:\n", df['label'].value_counts())

# Step 2: Prepare Data
print("\nPreparing data...")
def clean_text(text):
    if pd.isna(text):
        return ""
    text = re.sub(r'[^a-zA-Z\s]', '', str(text).lower())
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if w not in stop_words and len(w) > 2]
    return ' '.join(tokens)

# Combine title + text, clean
df['content'] = (df['title'].fillna('') + ' ' + df['text'].fillna('')).apply(clean_text)
df = df.dropna(subset=['content'])
df = df[df['content'].str.len() > 0]

# Features (X) and Target (y)
X = df['content']
y = df['label']

# Split 80/20
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Vectorize text to numbers (TF-IDF, top 5000 features)
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)
print("Training features shape:", X_train_vec.shape)

# Step 3: Train and Compare Models
print("\nTraining models...")
# Model 1: Decision Tree (Changed from Logistic)
dt_model = DecisionTreeClassifier(random_state=42, max_depth=10)  # Limited depth to avoid overfitting
dt_model.fit(X_train_vec, y_train)
dt_pred = dt_model.predict(X_test_vec)
dt_acc = accuracy_score(y_test, dt_pred)

# Model 2: Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf_model.fit(X_train_vec, y_train)
rf_pred = rf_model.predict(X_test_vec)
rf_acc = accuracy_score(y_test, rf_pred)

# Results
print("Decision Tree Accuracy:", round(dt_acc, 3))
print("Random Forest Accuracy:", round(rf_acc, 3))
print("\nDecision Tree Report:\n", classification_report(y_test, dt_pred, target_names=['Fake', 'Real']))

# Confusion Matrix Plot
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
sns.heatmap(confusion_matrix(y_test, dt_pred), annot=True, fmt='d', ax=axes[0], cmap='Blues')
axes[0].set_title('Decision Tree')
sns.heatmap(confusion_matrix(y_test, rf_pred), annot=True, fmt='d', ax=axes[1], cmap='Blues')
axes[1].set_title('Random Forest')
plt.savefig('confusion_matrix.png')  # Save for your slides!
# plt.show()  # Commented to avoid pop-up

# Pick Best (higher F1 for Fake—use '0' key since labels are numeric)
dt_report = classification_report(y_test, dt_pred, output_dict=True)
rf_report = classification_report(y_test, rf_pred, output_dict=True)
dt_f1 = dt_report['0']['f1-score']  # '0' = Fake
rf_f1 = rf_report['0']['f1-score']  # '0' = Fake
best_model = dt_model if dt_f1 > rf_f1 else rf_model
best_name = "Decision Tree" if dt_f1 > rf_f1 else "Random Forest"
print(f"\nBest Model: {best_name} (Fake F1: {max(dt_f1, rf_f1):.3f})")

# Save Both Models and Vectorizer (for live comparison in app)
joblib.dump(dt_model, 'dt_model.pkl')  # Save Decision Tree
joblib.dump(rf_model, 'rf_model.pkl')  # Save Random Forest (renamed for clarity)
joblib.dump(best_model, 'best_model.pkl')  # Save the winner
joblib.dump(vectorizer, 'vectorizer.pkl')
print("\nModels and vectorizer saved! Ready for API.")