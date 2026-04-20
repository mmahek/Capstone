"""
Evaluate All Trained Models - Loads saved models and compares
"""

import pandas as pd
import numpy as np
import pickle
import json
import os
import time
import re
from datetime import datetime

from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                            f1_score, roc_auc_score)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt
import seaborn as sns

print("=" * 80)
print("📊 EVALUATING ALL TRAINED MODELS")
print("=" * 80)

# ============================================
# 1. LOAD DATA
# ============================================
print("\n📂 Loading dataset...")
df = pd.read_csv("Symptom2Disease.csv")
df = df.drop("Unnamed: 0", axis=1)

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df['cleaned_text'] = df['text'].apply(clean_text)

# ============================================
# 2. LOAD SAVED VECTORIZER AND ENCODER
# ============================================
print("\n📂 Loading saved vectorizer and encoder...")

with open("models/trained/tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("models/trained/label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

X = vectorizer.transform(df['cleaned_text'])
y = label_encoder.transform(df['label'])

print(f"   Features: {X.shape[1]}")
print(f"   Classes: {len(label_encoder.classes_)}")

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ============================================
# 3. LOAD TRAINED MODELS AND EVALUATE
# ============================================
model_files = [f for f in os.listdir("models/trained") if f.endswith('.pkl') and f not in ['tfidf_vectorizer.pkl', 'label_encoder.pkl']]

print(f"\n📂 Found {len(model_files)} trained models")

results = []
cv_folds = 5
skf = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)

print("\n🧠 Evaluating models...")
print("-" * 80)

for model_file in model_files:
    model_name = model_file.replace('.pkl', '').replace('_', ' ').title()
    model_path = f"models/trained/{model_file}"
    
    print(f"\n▶ {model_name}")
    
    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        
        # Cross-validation
        cv_scores = cross_val_score(model, X_train, y_train, cv=skf, scoring='accuracy')
        
        # Predictions
        start_time = time.time()
        y_pred = model.predict(X_test)
        predict_time = time.time() - start_time
        
        # Get probabilities
        y_proba = None
        if hasattr(model, 'predict_proba'):
            y_proba = model.predict_proba(X_test)
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        roc_auc = None
        if y_proba is not None:
            try:
                roc_auc = roc_auc_score(y_test, y_proba, multi_class='ovr', average='weighted')
            except:
                pass
        
        results.append({
            'Model': model_name,
            'CV Mean': cv_scores.mean(),
            'CV Std': cv_scores.std(),
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'F1-Score': f1,
            'ROC-AUC': roc_auc,
            'Predict Time (s)': predict_time
        })
        
        print(f"   Accuracy: {accuracy:.4f} | F1: {f1:.4f}")
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:50]}")

# ============================================
# 4. CREATE RESULTS TABLE
# ============================================
results_df = pd.DataFrame(results)
results_df = results_df.sort_values('Accuracy', ascending=False)

print("\n" + "=" * 80)
print("📊 PERFORMANCE COMPARISON TABLE")
print("=" * 80)
print("\n")
print(results_df.to_string(index=False))

# ============================================
# 5. SAVE RESULTS
# ============================================
os.makedirs("evaluation", exist_ok=True)

results_df.to_csv("evaluation/model_comparison.csv", index=False)
results_df.to_json("evaluation/model_comparison.json", orient='records', indent=2)

# ============================================
# 6. VISUALIZATION
# ============================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Accuracy Bar Chart
ax1 = axes[0]
models_names = results_df['Model'].tolist()
accuracies = results_df['Accuracy'].tolist()
colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(models_names)))

bars = ax1.barh(models_names, accuracies, color=colors)
ax1.set_xlabel('Accuracy')
ax1.set_title('Model Accuracy Comparison')
ax1.set_xlim([0.6, 1.0])

for bar, acc in zip(bars, accuracies):
    ax1.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2, 
             f'{acc:.3f}', va='center', fontsize=9)

# Plot 2: Metrics Comparison
ax2 = axes[1]
metrics_df = results_df[['Model', 'Precision', 'Recall', 'F1-Score']].set_index('Model')
metrics_df.plot(kind='bar', ax=ax2)
ax2.set_title('Precision, Recall, and F1-Score Comparison')
ax2.set_ylabel('Score')
ax2.set_xlabel('')
ax2.legend(loc='lower right')
ax2.set_ylim([0.6, 1.0])
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.savefig("evaluation/model_comparison_charts.png", dpi=150, bbox_inches='tight')
print("\n✅ Saved: evaluation/model_comparison_charts.png")

# ============================================
# 7. LATEX TABLE
# ============================================
latex_table = """
\\begin{table}[h]
\\centering
\\caption{Performance Comparison of Machine Learning Models}
\\label{tab:model_comparison}
\\begin{tabular}{lcccc}
\\hline
\\textbf{Model} & \\textbf{Accuracy} & \\textbf{Precision} & \\textbf{Recall} & \\textbf{F1-Score} \\\\
\\hline
"""

for _, row in results_df.iterrows():
    latex_table += f"{row['Model']} & {row['Accuracy']:.4f} & {row['Precision']:.4f} & {row['Recall']:.4f} & {row['F1-Score']:.4f} \\\\\n"

latex_table += """\\hline
\\end{tabular}
\\end{table}
"""

with open("evaluation/latex_table.txt", "w") as f:
    f.write(latex_table)
print("✅ Saved: evaluation/latex_table.txt")

# ============================================
# 8. SUMMARY
# ============================================
print("\n" + "=" * 80)
print("📝 SUMMARY")
print("=" * 80)

best = results_df.iloc[0]
print(f"\n🏆 Best Model: {best['Model']}")
print(f"   Accuracy: {best['Accuracy']:.4f}")
print(f"   F1-Score: {best['F1-Score']:.4f}")

print("\n📁 All files saved to 'evaluation/' folder")
print("=" * 80)