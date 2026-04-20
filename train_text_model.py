"""
Train ML Model on Text-Based Symptom Descriptions
Using TF-IDF + XGBoost for lightweight inference
"""

import pandas as pd
import numpy as np
import pickle
import os
import json
import re
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb

print("=" * 60)
print("🏥 TRAINING TEXT-BASED SYMPTOM MODEL")
print("=" * 60)

# ---------------------------
# LOAD DATA
# ---------------------------
print("\n📂 Loading dataset...")
df = pd.read_csv("Symptom2Disease.csv")

# Drop unnecessary column
df = df.drop("Unnamed: 0", axis=1)

print(f"   Samples: {len(df)}")
print(f"   Unique diseases: {df['label'].nunique()}")

# ---------------------------
# TEXT CLEANING
# ---------------------------
def clean_text(text):
    """Clean symptom description text"""
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

print("\n🧹 Cleaning text...")
df['cleaned_text'] = df['text'].apply(clean_text)

# ---------------------------
# LABEL ENCODING
# ---------------------------
print("\n🏷️ Encoding labels...")
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(df['label'])

print(f"   Classes: {len(label_encoder.classes_)}")
print(f"   Sample labels: {list(label_encoder.classes_)[:5]}...")

# ---------------------------
# TF-IDF VECTORIZATION
# ---------------------------
print("\n📊 Creating TF-IDF features...")

vectorizer = TfidfVectorizer(
    max_features=500,
    stop_words='english',
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.9
)

X = vectorizer.fit_transform(df['cleaned_text'])
y = y_encoded

print(f"   Features: {X.shape[1]}")
print(f"   Classes: {len(np.unique(y))}")

# ---------------------------
# TRAIN XGBOOST
# ---------------------------
print("\n🧠 Training XGBoost model...")

model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    objective='multi:softprob',
    eval_metric='mlogloss',
    use_label_encoder=False,
    random_state=42,
    verbosity=0
)

# Train
model.fit(X, y)

# ---------------------------
# EVALUATE
# ---------------------------
print("\n📊 Evaluating model...")

# Cross-validation
cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f"   5-Fold CV Accuracy: {cv_scores.mean():.2%} (+/- {cv_scores.std():.2%})")

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
test_accuracy = accuracy_score(y_test, y_pred)
print(f"   Test Accuracy: {test_accuracy:.2%}")

# Classification report
print("\n📋 Classification Report:")
# Get actual class names for predictions
y_test_names = label_encoder.inverse_transform(y_test)
y_pred_names = label_encoder.inverse_transform(y_pred)
print(classification_report(y_test_names, y_pred_names, zero_division=0))

# ---------------------------
# SAVE MODEL
# ---------------------------
print("\n💾 Saving model...")
os.makedirs("models", exist_ok=True)

# Save XGBoost model
with open("models/xgb_text_model.pkl", "wb") as f:
    pickle.dump(model, f)

# Save vectorizer
with open("models/tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

# Save label encoder
with open("models/label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

# Save label mapping (for easy reference)
label_mapping = {str(i): name for i, name in enumerate(label_encoder.classes_)}
with open("models/label_mapping.json", "w", encoding='utf-8') as f:
    json.dump(label_mapping, f, indent=2)

# Save metadata
metadata = {
    "model_type": "XGBoost + TF-IDF",
    "n_samples": len(df),
    "n_features": X.shape[1],
    "n_classes": len(label_encoder.classes_),
    "cv_accuracy": float(cv_scores.mean()),
    "cv_std": float(cv_scores.std()),
    "test_accuracy": float(test_accuracy),
    "classes": list(label_encoder.classes_)
}

with open("models/model_metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

# Save class list for reference
with open("models/disease_classes.json", "w") as f:
    json.dump(list(label_encoder.classes_), f, indent=2)

model_size = os.path.getsize("models/xgb_text_model.pkl") / (1024 * 1024)

print(f"\n✅ Model saved!")
print(f"   📁 models/xgb_text_model.pkl ({model_size:.2f} MB)")
print(f"   📁 models/tfidf_vectorizer.pkl")
print(f"   📁 models/label_encoder.pkl")
print(f"   📁 models/label_mapping.json")
print(f"   📁 models/model_metadata.json")

print("\n" + "=" * 60)
print(f"🎉 TRAINING COMPLETE! Accuracy: {test_accuracy:.1%}")
print(f"   Model can predict {len(label_encoder.classes_)} different diseases")
print("=" * 60)