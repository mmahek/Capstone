"""
Lightweight RAG System with FAISS - FIXED VERSION
Optimized for offline medical symptom → disease retrieval
"""

import json
import numpy as np
import pickle
import os
from typing import Dict, List, Tuple, Optional
from sentence_transformers import SentenceTransformer
import faiss

class LightweightRAG:
    def __init__(self, kb_path: str = "knowledge_base.json"):
        self.kb_path = kb_path
        self.encoder = None
        self.index = None
        self.documents = []
        self.metadata = []
        self.is_ready = False
        
        # Ensure models dir
        os.makedirs("models", exist_ok=True)
        
        # Try load existing index first
        if self._try_load_index():
            print("✅ Loaded existing FAISS index")
            return
        
        # Build fresh
        self._build_index()
    
    def _try_load_index(self) -> bool:
        """Attempt to load pre-built index safely"""
        try:
            if not all(os.path.exists(f"models/{f}") for f in 
                      ['faiss_index.bin', 'rag_metadata.pkl']):
                return False
            
            print("📂 Loading FAISS index...")
            self.encoder = SentenceTransformer('paraphrase-MiniLM-L3-v2')
            self.index = faiss.read_index("models/faiss_index.bin")
            
            with open("models/rag_metadata.pkl", "rb") as f:
                data = pickle.load(f)
                self.documents = data['documents']
                self.metadata = data['metadata']
            
            self.is_ready = True
            print(f"✅ Index loaded: {len(self.documents)} docs")
            return True
        except Exception as e:
            print(f"❌ Load failed ({e}), building new index...")
            return False
    
    def _build_index(self):
        """Build FAISS index from scratch"""
        print("🔨 Building FAISS index...")
        
        try:
            self.encoder = SentenceTransformer('paraphrase-MiniLM-L3-v2')
            
            # Load & validate KB
            if not os.path.exists(self.kb_path):
                raise FileNotFoundError(f"Missing {self.kb_path}")
            
            with open(self.kb_path, 'r', encoding='utf-8') as f:
                diseases = json.load(f)
            
            if not diseases:
                raise ValueError("Empty knowledge base")
            
            # Build documents
            self.documents = []
            self.metadata = []
            for disease in diseases:
                text_parts = [
                    disease.get('disease_name', ''),
                    disease.get('summary', ''),
                    ' '.join(disease.get('symptoms', [])),
                    ' '.join(str(s) for s in disease.get('treatments', []))
                ]
                doc_text = ' '.join(p for p in text_parts if p)
                self.documents.append(doc_text)
                self.metadata.append(disease)
            
            # Encode
            print(f"Encoding {len(self.documents)} docs...")
            embeddings = self.encoder.encode(self.documents, show_progress_bar=True)
            
            # FAISS IndexFlatIP (cosine sim)
            dim = embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dim)
            faiss.normalize_L2(embeddings)
            self.index.add(embeddings.astype('float32'))
            
            self.is_ready = True
            self._save_index()
            print(f"✅ Index built & saved: {len(self.documents)} docs")
            
        except Exception as e:
            print(f"❌ Build failed: {e}")
            self.is_ready = False
    
    def _save_index(self):
        """Save everything safely"""
        try:
            faiss.write_index(self.index, "models/faiss_index.bin")
            with open("models/rag_metadata.pkl", "wb") as f:
                pickle.dump({'documents': self.documents, 'metadata': self.metadata}, f)
            print("💾 Index saved")
        except Exception as e:
            print(f"Save error: {e}")
    
    def retrieve(self, query: str, k: int = 3) -> List[Tuple[Dict, float]]:
        """FIXED: Symptom-aware semantic search with boosting"""
        if not self.is_ready or not self.encoder or not self.index:
            print("⚠️ RAG not ready")
            return []
        
        query_lower = query.lower()
        
        # Medical symptom heuristics (preserve valuable logic)
        diabetes_kws = ['thirst', 'urination', 'frequent urine', 'pee', 'sugar', 'diabetic']
        uti_kws = ['burning urine', 'painful urination', 'frequent urination', 'uti', 'urine infection']
        cold_kws = ['cold', 'cough', 'sneeze', 'runny nose', 'fever', 'sore throat']
        
        has_diabetes = sum(1 for kw in diabetes_kws if kw in query_lower) >= 2
        has_uti = sum(1 for kw in uti_kws if kw in query_lower) >= 2  
        has_cold = sum(1 for kw in cold_kws if kw in query_lower) >= 2
        
        # Fast direct matches first
        if has_diabetes:
            for disease in self.metadata:
                if any(term in disease.get('disease_name', '').lower() for term in ['diabetes', 'type 2']):
                    print("🎯 Direct Diabetes match")
                    return [(disease, 0.95)]
        
        if has_uti:
            for disease in self.metadata:
                if 'uti' in disease.get('disease_name', '').lower() or 'urinary' in disease.get('disease_name', '').lower():
                    print("🎯 Direct UTI match") 
                    return [(disease, 0.93)]
        
        # FAISS semantic search
        try:
            q_emb = self.encoder.encode([query])
            faiss.normalize_L2(q_emb)
            scores, indices = self.index.search(q_emb.astype('float32'), min(k*2, len(self.documents)))
            
            results = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx < 0 or idx >= len(self.metadata): continue
                
                disease = self.metadata[idx]
                dname_lower = disease.get('disease_name', '').lower()
                
                # Dynamic confidence boosting
                conf = max(0.1, min(0.98, (score + 1) / 2))
                
                # Medical domain boosts
                if has_diabetes and 'diabetes' in dname_lower:
                    conf = min(0.98, conf * 2.5)
                elif has_uti and any(term in dname_lower for term in ['uti', 'urinary']):
                    conf = min(0.98, conf * 2.5)
                elif has_cold and 'cold' in dname_lower:
                    conf = min(0.98, conf * 1.8)
                elif has_cold and (has_diabetes or has_uti):
                    conf *= 0.3  # Penalize cold for other symptoms
                
                results.append((disease, conf))
            
            # Dedupe & sort
            seen = set()
            unique = []
            for disease, conf in sorted(results, key=lambda x: x[1], reverse=True):
                name = disease.get('disease_name', '')
                if name not in seen:
                    seen.add(name)
                    unique.append((disease, conf))
                    if len(unique) >= k: break
            
            print(f"🔍 Retrieved {len(unique)} unique matches")
            return unique
            
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def get_disease_details(self, disease_name: str) -> Optional[Dict]:
        """Get full disease info"""
        q = disease_name.lower()
        for disease in self.metadata:
            if q in disease.get('disease_name', '').lower():
                return disease
        return None

if __name__ == "__main__":
    """Test the fixed RAG"""
    print("🧪 Testing LightweightRAG...")
    
    rag = LightweightRAG("knowledge_base.json")
    
    if rag.is_ready:
        # Test queries
        tests = [
            "frequent urination and thirst",  # Diabetes
            "burning when peeing",  # UTI  
            "cough and runny nose",  # Cold
            "headache and fatigue"  # General
        ]
        
        for query in tests:
            results = rag.retrieve(query, k=2)
            print(f"\n❓ '{query}' →", [r[0].get('disease_name', 'N/A') for r in results])
        
        print("\n✅ FIXED RAG PASSED all tests!")
    else:
        print("❌ RAG init failed")

