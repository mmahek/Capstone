"""
Medical Knowledge Base Loader with Improved Matching
"""

import json
import os
from typing import Dict, List, Tuple

class KnowledgeBase:
    def __init__(self, kb_path: str):
        self.knowledge = []
        self.disease_names = []
        self.symptom_to_disease = {}  # Reverse index for faster matching
        self.load(kb_path)
        self._build_index()
    
    def load(self, path: str):
        """Load knowledge_base.json"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                if isinstance(data, list):
                    self.knowledge = data
                elif isinstance(data, dict):
                    self.knowledge = list(data.values())
                
                self.disease_names = [d.get('disease_name', '') for d in self.knowledge]
                print(f"✅ Loaded {len(self.knowledge)} diseases")
        except Exception as e:
            print(f"❌ Error loading KB: {e}")
            self.knowledge = self._fallback()
            self.disease_names = [d.get('disease_name', '') for d in self.knowledge]
    
    def _build_index(self):
        """Build reverse index: symptom -> diseases"""
        for disease in self.knowledge:
            disease_name = disease.get('disease_name', '')
            for symptom in disease.get('symptoms', []):
                symptom_lower = symptom.lower()
                if symptom_lower not in self.symptom_to_disease:
                    self.symptom_to_disease[symptom_lower] = []
                self.symptom_to_disease[symptom_lower].append(disease_name)
    
    def _fallback(self) -> List[Dict]:
        return [{
            "disease_name": "Sample Disease",
            "summary": "Knowledge base not found",
            "symptoms": [],
            "precautions": [],
            "when_to_see_doctor": "Consult healthcare provider"
        }]
    
    def get_by_name(self, disease_name: str) -> Dict:
        """Get disease by exact name"""
        for disease in self.knowledge:
            if disease.get('disease_name', '').lower() == disease_name.lower():
                return disease
        return None
    
    def search_keyword(self, query: str) -> Tuple[Dict, int]:
        """Improved keyword-based search with symptom weighting"""
        query_lower = query.lower()
        disease_scores = {}
        
        # Split query into words for better matching
        query_words = query_lower.split()
        
        for disease in self.knowledge:
            disease_name = disease.get('disease_name', '')
            score = 0
            
            # Disease name match (highest weight)
            if disease_name.lower() in query_lower:
                score += 15
            
            # Symptom matching
            symptoms = disease.get('symptoms', [])
            for symptom in symptoms:
                symptom_lower = symptom.lower()
                
                # Exact symptom match
                if symptom_lower in query_lower:
                    score += 5
                # Partial match (e.g., "itch" matches "itching")
                elif any(word in symptom_lower or symptom_lower in word for word in query_words):
                    score += 2
            
            # Special symptom groups
            if any(w in query_lower for w in ['urination', 'urine', 'pee']) and any(w in disease_name.lower() for w in ['uti', 'urinary', 'diabetes']):
                score += 8
            if any(w in query_lower for w in ['thirst', 'thirsty']) and 'diabetes' in disease_name.lower():
                score += 8
            if any(w in query_lower for w in ['itch', 'itching', 'rash']) and any(w in disease_name.lower() for w in ['allergy', 'dermatitis', 'eczema']):
                score += 5
            
            if score > 0:
                disease_scores[disease_name] = score
        
        # Get best match
        if disease_scores:
            best_disease_name = max(disease_scores, key=disease_scores.get)
            best_score = disease_scores[best_disease_name]
            best_match = self.get_by_name(best_disease_name)
            
            # Cap max score for confidence calculation
            max_possible = 30
            return best_match, min(best_score, max_possible)
        
        return None, 0