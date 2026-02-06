Learning_Path_Recommender
An AI-powered web application that analyzes a user’s resume and career goal to generate a **personalized 6-month learning roadmap using **Retrieval-Augmented Generation (RAG) and LLMs*

 🧠 GenAI Learning Path Recommender

An AI-powered web application that analyzes a user’s resume and career goal to generate a **personalized 6-month learning roadmap** using **Retrieval-Augmented Generation (RAG)** and **LLMs**.

---

🚀 Features
- Upload resume (PDF)
- Define career goal (e.g., “Become a GenAI Engineer”)
- AI analyzes skill gaps
- Generates structured learning roadmap
- Uses only curated, real-world courses
- Token optimization with ScaleDown (fallback supported)

---

🧠 Architecture Overview

1. **Resume Parsing**
   - Extracts text from PDF using PyMuPDF

2. **Context Building**
   - Combines resume + goal + curated course dataset

3. **Prompt Optimization**
   - Uses ScaleDown API to reduce token usage (with graceful fallback)

4. **LLM Reasoning**
   - Gemini model generates roadmap using optimized context

5. **Output Layer**
   - Displays roadmap and allows download

---

🔁 AI Pipeline
Resume PDF + Goal
↓
Text Extraction
↓
Context Assembly (Resume + Courses)
↓
Prompt Optimization (ScaleDown)
↓
LLM Reasoning (Gemini)
↓
Personalized Learning Roadmap


---

## 🛠 Tech Stack
- Python
- Streamlit
- Gemini (Google Generative AI)
- ScaleDown API
- RAG-style context grounding
- PyMuPDF

---

## ▶️ How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py

