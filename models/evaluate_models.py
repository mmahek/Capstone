"""
Evaluate and Compare Models
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import json
import os

print("=" * 70)
print("📊 MODEL EVALUATION REPORT")
print("=" * 70)

# Load data
print("\n📂 Loading dataset...")
df = pd.read_csv("Symptom2Disease.csv")
df = df.fillna(0)

# Find target column
target_col = None
for col in df.columns:
    if col.lower() in ['disease', 'prognosis', 'target', 'label']:
        target_col = col
        break
if target_col is None:
    target_col = df.columns[-1]

print(f"   Target column: '{target_col}'")

X = df.drop(target_col, axis=1)
X = X.apply(pd.to_numeric, errors='coerce').fillna(0)
y = df[target_col]

# Feature selection
from sklearn.feature_selection import VarianceThreshold
selector = VarianceThreshold(threshold=0.01)
X_reduced = selector.fit_transform(X)

print(f"   Samples: {len(X)}")
print(f"   Features: {X_reduced.shape[1]}")
print(f"   Diseases: {y.nunique()}")

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X_reduced, y, test_size=0.2, random_state=42, stratify=y
)

# Models to evaluate
models = {
    'XGBoost': xgb.XGBClassifier(
        n_estimators=150, max_depth=6, learning_rate=0.1,
        subsample=0.8, colsample_bytree=0.8, random_state=42,
        use_label_encoder=False, eval_metric='mlogloss', verbosity=0
    ),
    'Random Forest': RandomForestClassifier(
        n_estimators=150, max_depth=10, random_state=42, n_jobs=-1
    )
}

# Try to import LightGBM (optional)
try:
    import lightgbm as lgb
    models['LightGBM'] = lgb.LGBMClassifier(
        n_estimators=150, max_depth=6, learning_rate=0.1,
        subsample=0.8, colsample_bytree=0.8, random_state=42, verbose=-1
    )
except ImportError:
    print("   ⚠️ LightGBM not installed, skipping...")

# Evaluate
results = {}
print("\n🧠 Training and evaluating models...")
print("-" * 50)

for name, model in models.items():
    print(f"\n▶ {name}")
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
    print(f"   CV Accuracy: {cv_scores.mean():.2%} (+/- {cv_scores.std():.2%})")
    
    # Train and test
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    test_acc = accuracy_score(y_test, y_pred)
    print(f"   Test Accuracy: {test_acc:.2%}")
    
    results[name] = {
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std(),
        'test_accuracy': test_acc,
        'model': model
    }

# Save results
os.makedirs("evaluation", exist_ok=True)

# Bar chart
plt.figure(figsize=(10, 6))
names = list(results.keys())
accuracies = [results[n]['test_accuracy'] * 100 for n in names]
colors = ['#0D9488', '#0284C7', '#F59E0B'][:len(names)]

plt.bar(names, accuracies, color=colors)
plt.ylabel('Accuracy (%)')
plt.title('Model Accuracy Comparison')
plt.ylim([80, 100])
for i, v in enumerate(accuracies):
    plt.text(i, v + 0.5, f"{v:.1f}%", ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig("evaluation/model_comparison.png", dpi=150)
print("\n   ✅ Saved: evaluation/model_comparison.png")

# Report
best_name = max(results, key=lambda x: results[x]['test_accuracy'])
report = {
    'dataset_info': {'samples': len(X), 'features': X_reduced.shape[1], 'diseases': y.nunique()},
    'best_model': best_name,
    'best_accuracy': float(results[best_name]['test_accuracy'])
}

with open("evaluation/evaluation_report.json", "w") as f:
    json.dump(report, f, indent=2)

print(f"\n🏆 Best Model: {best_name} ({results[best_name]['test_accuracy']:.2%})")
print("=" * 70)