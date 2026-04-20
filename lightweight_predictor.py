"""
Lightweight Predictor for Text Symptoms
"""

import pickle
import re
import numpy as np
from typing import Tuple, Dict

class SymptomPredictor:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.label_encoder = None
        self.classes = []
        self.is_ready = False
        
        try:
            with open("models/xgb_text_model.pkl", "rb") as f:
                self.model = pickle.load(f)
            with open("models/tfidf_vectorizer.pkl", "rb") as f:
                self.vectorizer = pickle.load(f)
            with open("models/label_encoder.pkl", "rb") as f:
                self.label_encoder = pickle.load(f)
            
            self.classes = list(self.label_encoder.classes_)
            self.is_ready = True
            print(f"✅ Model loaded ({len(self.classes)} diseases)")
        except Exception as e:
            print(f"⚠️ Model not loaded: {e}")
    
    def clean_text(self, text: str) -> str:
        """Clean input text"""
        text = str(text).lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def predict(self, symptoms: str) -> Tuple[str, float, Dict]:
        """Predict disease from symptom text"""
        if not self.is_ready:
            return "Unknown", 0.0, {}
        
        # Clean and vectorize
        cleaned = self.clean_text(symptoms)
        vector = self.vectorizer.transform([cleaned])
        
        # Predict
        probabilities = self.model.predict_proba(vector)[0]
        
        # Top 3 predictions
        top_indices = np.argsort(probabilities)[-3:][::-1]
        top_predictions = {
            self.label_encoder.inverse_transform([idx])[0]: float(probabilities[idx])
            for idx in top_indices
        }
        
        # Best prediction
        best_idx = np.argmax(probabilities)
        best_disease = self.label_encoder.inverse_transform([best_idx])[0]
        best_confidence = float(probabilities[best_idx])
        
        return best_disease, best_confidence, top_predictions