"""
Hybrid Chatbot - Text ML + RAG
"""

import json
import os
from typing import Dict, Optional
from lightweight_predictor import SymptomPredictor
from lightweight_rag import LightweightRAG

class LightweightHybridChatbot:
    def __init__(self):
        # Load text-based ML model
        self.ml = SymptomPredictor()
        self.ml_ready = self.ml.is_ready
        
        # Load RAG
        self.rag = LightweightRAG()
        
        # Load knowledge base
        with open("knowledge_base.json", "r", encoding='utf-8') as f:
            self.kb = json.load(f)
        
        self.ML_CONFIDENCE_THRESHOLD = 0.60
        self.last_disease = None
    
    def process(self, symptoms: str) -> Dict:
        """Process symptoms and return prediction"""
        
        result = {
            'disease': None,
            'source': None,
            'confidence': 0.0,
            'method': None
        }
        
        # Try ML prediction
        if self.ml_ready:
            ml_disease, ml_conf, top_ml = self.ml.predict(symptoms)
            
            if ml_conf >= self.ML_CONFIDENCE_THRESHOLD:
                # ML confident - find in KB
                disease_info = self._find_in_kb(ml_disease)
                if disease_info:
                    result['disease'] = disease_info
                    result['source'] = "AI Model"
                    result['confidence'] = ml_conf
                    result['method'] = 'ml'
                    self.last_disease = disease_info
                    return result
        
        # Fallback to RAG
        rag_results = self.rag.retrieve(symptoms, k=3)
        if rag_results:
            result['disease'] = rag_results[0][0]
            result['source'] = "Medical Encyclopedia"
            result['confidence'] = rag_results[0][1]
            result['method'] = 'rag'
            self.last_disease = rag_results[0][0]
        else:
            result['disease'] = {
                'disease_name': 'Uncertain',
                'summary': 'Please describe your symptoms more clearly.',
                'precautions': ['Consult a healthcare provider']
            }
            result['source'] = "Fallback"
            result['method'] = 'fallback'
        
        return result
    
    def _find_in_kb(self, disease_name: str) -> Optional[Dict]:
        """Find disease in knowledge base"""
        for disease in self.kb:
            if disease.get('disease_name', '').lower() == disease_name.lower():
                return disease
        return None