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

bash
pip install -r requirements.txt
streamlit run app.py


ScreenShots: 
<img width="1918" height="1032" alt="screenshot1" src="https://github.com/user-attachments/assets/c88194e5-24e4-48fc-b881-4c04609a0eea" />
<img width="1914" height="1036" alt="screenshot2" src="https://github.com/user-attachments/assets/8084044c-4c96-4092-b768-4c3a939662c3" />
<img width="1919" height="935" alt="screenshot3" src="https://github.com/user-attachments/assets/1a3a220b-3a32-451a-b049-6e391f676dd3" />
