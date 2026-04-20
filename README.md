# 🏥 स्वास्थ्य साथी | Health Companion

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red.svg)](https://streamlit.io/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0.0-green.svg)](https://xgboost.readthedocs.io/)
[![FAISS](https://img.shields.io/badge/FAISS-1.7.4-orange.svg)](https://github.com/facebookresearch/faiss)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **AI-Powered Rural Healthcare Chatbot with Hybrid ML-RAG Architecture**

A bilingual (Hindi/English), privacy-first health assistant designed for low-connectivity rural India. Combines XGBoost machine learning with FAISS-powered retrieval-augmented generation for accurate, context-aware health guidance.

---

## ✨ Features

### 🧠 Intelligent Symptom Analysis

* Hybrid ML-RAG Architecture (XGBoost + FAISS)
* 24 Disease Classes
* Confidence-based fallback system

### 🌍 Environmental Intelligence

* Weather-aware health suggestions
* Location-based risk adjustments
* Offline fallback support

### 🗣️ Bilingual & Accessible

* Hindi + English support
* Voice input support
* Severity slider (1–10 scale)

### 📶 Rural-First Design

* Low bandwidth optimized
* Lightweight (~2.2 MB model)
* Offline knowledge base

### 🔒 Privacy & Safety

* No data storage
* In-memory processing
* Educational (non-diagnostic)

---

## 🏗️ Architecture

* **ML Layer**: XGBoost classifier
* **RAG Layer**: FAISS + Sentence Transformers
* **Router**: Confidence-based switching
* **Context Layer**: Weather + Severity + KB

---

## 🛠️ Tech Stack

| Category | Tech                         |
| -------- | ---------------------------- |
| Frontend | Streamlit                    |
| ML       | XGBoost, scikit-learn        |
| RAG      | FAISS, Sentence Transformers |
| API      | OpenWeatherMap               |
| Data     | Pandas, NumPy                |

---

## 🚀 Quick Start

### 1. Clone repo

```bash
git clone https://github.com/yourusername/health-companion-chatbot.git
cd health-companion-chatbot
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Train model

```bash
python train_text_model.py
```

### 5. Build FAISS index

```bash
python lightweight_rag.py
```

### 6. Run app

```bash
streamlit run app.py
```

---

## 📦 Model & Cache Files

Large files such as trained models, FAISS index, and cache are **NOT included** in this repository due to GitHub size limits.

👉 To regenerate them:

```bash
python train_text_model.py
python lightweight_rag.py
```

This keeps the repository lightweight and reproducible.

---

## 📁 Project Structure

```
health-companion-chatbot/
│
├── app.py
├── config.py
├── lightweight_rag.py
├── lightweight_predictor.py
├── hybrid_chatbot_lightweight.py
├── knowledge_base.py
├── severity_classifier.py
│
├── data/
├── models/ (generated)
├── cache/ (ignored)
│
├── train_text_model.py
├── requirements.txt
└── README.md
```

---

## 📊 Performance

* XGBoost Accuracy: **87.5%**
* Hybrid System Accuracy: **~92%**
* Model Size: **2.2 MB**
* Response Time: **< 2 sec**

---

## 🌍 Unique Points

* Built for rural India 🇮🇳
* Works in low connectivity
* Bilingual (Hindi + English)
* Privacy-first design

---

## 🤝 Contributing

1. Fork repo
2. Create branch
3. Commit changes
4. Open PR

---

## 📄 License

MIT License

---

## 📞 Contact

* GitHub: https://github.com/yourusername
* Email: [your.email@example.com](mailto:your.email@example.com)

---

⭐ If you found this useful, consider giving a star!
