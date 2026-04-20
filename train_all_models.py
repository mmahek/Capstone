"""
Train All ML Models for Research Paper Comparison
Saves each trained model for later evaluation
"""

import pandas as pd
import numpy as np
import pickle
import os
import re
import json
from datetime import datetime

# Preprocessing
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

# Models
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostClassifier

print("=" * 80)
print("🏥 TRAINING ALL ML MODELS FOR RESEARCH PAPER")
print("=" * 80)

# ============================================
# 1. LOAD AND PREPARE DATA
# ============================================
print("\n📂 Loading dataset...")
df = pd.read_csv("Symptom2Disease.csv")
df = df.drop("Unnamed: 0", axis=1)

print(f"   Samples: {len(df)}")
print(f"   Classes: {df['label'].nunique()}")
print(f"   Sample labels: {df['label'].unique()[:5]}")

# Clean text
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

print("\n🧹 Cleaning text...")
df['cleaned_text'] = df['text'].apply(clean_text)

# ============================================
# 2. TF-IDF VECTORIZATION
# ============================================
print("\n📊 Creating TF-IDF features...")
vectorizer = TfidfVectorizer(
    max_features=500,
    stop_words='english',
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.9
)

X = vectorizer.fit_transform(df['cleaned_text'])
y = df['label']

print(f"   Features: {X.shape[1]}")
print(f"   Classes: {y.nunique()}")

# ============================================
# 3. LABEL ENCODING
# ============================================
print("\n🏷️ Encoding labels...")
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

print(f"   Encoded classes: {len(label_encoder.classes_)}")

# ============================================
# 4. TRAIN/TEST SPLIT
# ============================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

print(f"\n📊 Data Split:")
print(f"   Training samples: {X_train.shape[0]}")
print(f"   Testing samples: {X_test.shape[0]}")

# ============================================
# 5. DEFINE MODELS
# ============================================
models = {
    'XGBoost': xgb.XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        use_label_encoder=False,
        eval_metric='mlogloss',
        random_state=42,
        verbosity=0
    ),
    
    'LightGBM': lgb.LGBMClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        verbose=-1
    ),
    
    'CatBoost': CatBoostClassifier(
        iterations=100,
        depth=5,
        learning_rate=0.1,
        random_seed=42,
        verbose=0
    ),
    
    'RandomForest': RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    ),
    
    'LogisticRegression': LogisticRegression(
        max_iter=1000,
        random_state=42,
        n_jobs=-1
    ),
    
    'SVM': SVC(
        kernel='linear',
        probability=True,
        random_state=42
    ),
    
    'NaiveBayes': MultinomialNB(),
    
    'NeuralNetwork': MLPClassifier(
        hidden_layer_sizes=(100, 50),
        max_iter=500,
        random_state=42,
        early_stopping=True
    )
}

# ============================================
# 6. TRAIN ALL MODELS
# ============================================
print("\n" + "=" * 80)
print("🧠 TRAINING MODELS")
print("=" * 80)

os.makedirs("models/trained", exist_ok=True)

training_results = []

for name, model in models.items():
    print(f"\n▶ Training {name}...")
    
    try:
        # Train model
        model.fit(X_train, y_train)
        
        # Save model
        model_path = f"models/trained/{name.lower().replace(' ', '_')}.pkl"
        with open(model_path, "wb") as f:
            pickle.dump(model, f)
        
        # Quick accuracy check
        train_acc = model.score(X_train, y_train)
        test_acc = model.score(X_test, y_test)
        
        print(f"   ✅ Train Accuracy: {train_acc:.4f}")
        print(f"   ✅ Test Accuracy: {test_acc:.4f}")
        print(f"   💾 Saved: {model_path}")
        
        training_results.append({
            'Model': name,
            'Train Accuracy': train_acc,
            'Test Accuracy': test_acc,
            'Saved Path': model_path
        })
        
    except Exception as e:
        print(f"   ❌ Error training {name}: {str(e)[:100]}")

# ============================================
# 7. SAVE VECTORIZER AND ENCODER
# ============================================
print("\n💾 Saving vectorizer and encoder...")

with open("models/trained/tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open("models/trained/label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

print("   ✅ Saved: models/trained/tfidf_vectorizer.pkl")
print("   ✅ Saved: models/trained/label_encoder.pkl")

# ============================================
# 8. SAVE TRAINING METADATA
# ============================================
metadata = {
    'dataset': 'Symptom2Disease',
    'samples': len(df),
    'features': X.shape[1],
    'classes': len(label_encoder.classes_),
    'class_names': label_encoder.classes_.tolist(),
    'train_date': datetime.now().isoformat(),
    'training_results': training_results
}

with open("models/trained/training_metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print("   ✅ Saved: models/trained/training_metadata.json")

# ============================================
# 9. SUMMARY
# ============================================
print("\n" + "=" * 80)
print("📊 TRAINING SUMMARY")
print("=" * 80)

print("\nModel Performance on Test Set:")
print("-" * 50)
for result in sorted(training_results, key=lambda x: x['Test Accuracy'], reverse=True):
    print(f"   {result['Model']:20} → {result['Test Accuracy']:.4f}")

best = max(training_results, key=lambda x: x['Test Accuracy'])
print(f"\n🏆 Best Model: {best['Model']} ({best['Test Accuracy']:.4f})")

print("\n" + "=" * 80)
print("✅ ALL MODELS TRAINED AND SAVED!")
print("=" * 80)
print("\n📁 Models saved to: models/trained/")
print("   Run 'python evaluate_all_models.py' to generate comparison charts")