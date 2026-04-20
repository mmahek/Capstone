"""
Symptom Severity Classifier
"""

import re
from typing import Tuple

class SeverityClassifier:
    def __init__(self):
        self.critical = [
            "chest pain", "difficulty breathing", "bleeding", "stroke",
            "heart attack", "unconscious", "seizure", "cannot breathe"
        ]
        self.high = [
            "high fever", "severe", "extreme", "vomiting blood",
            "confusion", "severe headache", "blood in stool"
        ]
        self.moderate = [
            "fever", "vomiting", "diarrhea", "persistent",
            "headache", "body aches", "fatigue", "weakness"
        ]
    
    def classify(self, text: str) -> Tuple[str, int]:
        """Classify severity: low, moderate, high"""
        text_lower = text.lower()
        score = 0
        
        for kw in self.critical:
            if kw in text_lower:
                score += 10
                break
        
        for kw in self.high:
            if kw in text_lower:
                score += 5
        
        for kw in self.moderate:
            if kw in text_lower:
                score += 2
        
        # Check for fever temperature
        temp_match = re.search(r'(\d+\.?\d*)\s*(?:degree|°|fever)', text_lower)
        if temp_match:
            temp = float(temp_match.group(1))
            if temp > 103:
                score += 5
            elif temp > 101:
                score += 2
        
        # Check duration
        days_match = re.search(r'(\d+)\s*days', text_lower)
        if days_match and int(days_match.group(1)) > 7:
            score += 3
        
        if score >= 10:
            return "high", score
        elif score >= 5:
            return "moderate", score
        return "low", score
    
    def get_advice(self, severity: str) -> str:
        """Get advice based on severity"""
        advice = {
            'high': "🚨 SEEK IMMEDIATE MEDICAL ATTENTION",
            'moderate': "⚠️ Monitor closely. Consult doctor if worsens.",
            'low': "✅ Self-care should be sufficient."
        }
        return advice.get(severity, "")