"""
Build RAG Index from Knowledge Base
"""

from lightweight_rag import LightweightRAG

print("=" * 50)
print("🔨 Building RAG Index")
print("=" * 50)

# This will create and save the FAISS index
rag = LightweightRAG("knowledge_base.json")

print("\n✅ RAG index built successfully!")
print("   📁 models/faiss_index.bin")
print("   📁 models/rag_metadata.pkl")
print("   📁 models/rag_embeddings.npy")