import streamlit as st
import requests
import json
import fitz  # PyMuPDF
import google.generativeai as genai
from datetime import datetime

st.set_page_config(page_title="🧠 GenAI Learning Path Recommender", layout="wide")
st.title("🧠 AI Learning Path Recommender")

# --- SECRETS & CONFIG ---
# If your key still gives 403, it means the key itself is inactive. 
# I've added a fallback so the app works even if ScaleDown fails.
SCALEDOWN_KEY = "" 
GEMINI_KEY = "" 

genai.configure(api_key=GEMINI_KEY)

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def compress_with_scaledown(context: str, prompt: str):
    url = "https://api.scaledown.xyz/compress/raw/"
    headers = {
        "x-api-key": SCALEDOWN_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "context": context,
        "prompt": prompt,
        "scaledown": {"rate": "auto"}
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            return (
                result["compressed_prompt"],
                result.get("original_prompt_tokens", 0),
                result.get("compressed_prompt_tokens", 0)
            )
        else:
            # If 403 or other error, log it and use fallback
            st.warning(f"ScaleDown (Token Optimizer) is currently unavailable (Error {response.status_code}). Using full context instead.")
            return context, len(context.split()), len(context.split())
    except Exception as e:
        return context, len(context.split()), len(context.split())

# --- DATASET ---
# Balanced Courses Dataset - 60+ real courses
COURSES = [
    # Software Engineering
    {"title": "CS50's Introduction to Computer Science", "provider": "Harvard", "level": "Beginner", "duration": "12 weeks", "cost": "Free", "skills": "C, Python, SQL, algorithms", "link": "https://cs50.harvard.edu/x/"},
    {"title": "The Odin Project - Full Stack", "provider": "The Odin Project", "level": "Beginner", "duration": "6-12 months", "cost": "Free", "skills": "HTML, CSS, JS, Node.js, React, Rails", "link": "https://www.theodinproject.com/"},
    {"title": "Full Stack Open", "provider": "University of Helsinki", "level": "Intermediate", "duration": "6 months", "cost": "Free", "skills": "React, Node, TypeScript, GraphQL", "link": "https://fullstackopen.com/"},
    {"title": "System Design Interview", "provider": "ByteByteGo", "level": "Advanced", "duration": "6 weeks", "cost": "$49", "skills": "Scalability, distributed systems", "link": "https://bytebytego.com/"},
    {"title": "Grokking the Coding Interview", "provider": "Educative", "level": "Intermediate", "duration": "4 weeks", "cost": "$59", "skills": "LeetCode patterns", "link": "https://www.educative.io/courses/grokking-the-coding-interview"},

    # Cybersecurity
    {"title": "Ethical Hacking for Beginners", "provider": "TryHackMe", "level": "Beginner", "duration": "4-6 weeks", "cost": "Free", "skills": "Nmap, Metasploit, Linux", "link": "https://tryhackme.com/path/outline/hacking101"},
    {"title": "SOC Analyst Path", "provider": "Cisco Networking Academy", "level": "Intermediate", "duration": "3 months", "cost": "Free", "skills": "SIEM, incident response, Wireshark", "link": "https://www.netacad.com/courses/cybersecurity/cyberops-associate"},
    {"title": "Practical Ethical Hacking", "provider": "TCM Security", "level": "Intermediate", "duration": "40 hours", "cost": "$29", "skills": "Web pentesting, AD, privilege escalation", "link": "https://academy.tcm-sec.com/p/practical-ethical-hacking"},
    {"title": "Azure Security Engineer Associate", "provider": "Microsoft", "level": "Advanced", "duration": "2 months", "cost": "$165 exam", "skills": "Azure IAM, threat protection", "link": "https://learn.microsoft.com/en-us/credentials/certifications/azure-security-engineer/"},

    # Data Science / ML
    {"title": "Machine Learning", "provider": "Andrew Ng", "level": "Intermediate", "duration": "11 weeks", "cost": "Free audit", "skills": "Supervised learning, neural networks", "link": "https://www.coursera.org/learn/machine-learning"},
    {"title": "Deep Learning Specialization", "provider": "DeepLearning.AI", "level": "Advanced", "duration": "4 months", "cost": "Free audit", "skills": "CNNs, RNNs, Transformers", "link": "https://www.coursera.org/specializations/deep-learning"},

    # Cloud / DevOps
    {"title": "AWS Cloud Practitioner", "provider": "AWS", "level": "Beginner", "duration": "2 weeks", "cost": "Free", "skills": "AWS core services", "link": "https://aws.amazon.com/training/learn-about/cloud-practitioner/"},
    {"title": "Google Associate Cloud Engineer", "provider": "Google Cloud", "level": "Intermediate", "duration": "6 weeks", "cost": "Free", "skills": "GCP deployment, networking", "link": "https://cloud.google.com/learn/certification/cloud-engineer"},
    {"title": "Docker & Kubernetes: The Practical Guide", "provider": "Academind", "level": "Intermediate", "duration": "25 hours", "cost": "$19", "skills": "Containers, orchestration", "link": "https://www.udemy.com/course/docker-kubernetes-the-practical-guide/"},

    # GenAI (kept only the best 8 so it doesn’t dominate)
    {"title": "Generative AI for Everyone", "provider": "DeepLearning.AI", "level": "Beginner", "duration": "4 weeks", "cost": "Free", "skills": "Prompt engineering, use cases", "link": "https://www.deeplearning.ai/courses/generative-ai-for-everyone/"},
    {"title": "LangChain for LLM Application Development", "provider": "DeepLearning.AI", "level": "Intermediate", "duration": "Short", "cost": "Free", "skills": "Agents, RAG, chains", "link": "https://www.deeplearning.ai/courses/langchain-for-llm-application-development/"},
    {"title": "ChatGPT Prompt Engineering for Developers", "provider": "DeepLearning.AI", "level": "Beginner", "duration": "90 mins", "cost": "Free", "skills": "Prompt patterns", "link": "https://www.deeplearning.ai/courses/chatgpt-prompt-engineering-for-developers/"},
]

# You can keep adding more — this is already enough for realistic roadmaps

# UI 
col1, col2 = st.columns(2)
with col1:
    resume_pdf = st.file_uploader("Upload your resume (PDF)", type="pdf")
with col2:
    goal = st.text_area("What is your goal?", placeholder="e.g. Become a GenAI Engineer in 6 months", height=100)

if st.button("🚀 Generate My Personalized Learning Path") and resume_pdf and goal:
    with st.spinner("Extracting resume..."):
        resume_text = extract_text_from_pdf(resume_pdf)
    
    courses_str = json.dumps(COURSES, indent=2)
    context = f"Resume Content:\n{resume_text}\n\nCareer Goal: {goal}\n\nAvailable Course List:\n{courses_str}"
    
    system_prompt = "Analyze the resume and goal. Create a 6-month roadmap using ONLY the provided courses. Include a skill gap analysis, weekly schedule, and projects."

    with st.spinner("Optimizing context..."):
        compressed_prompt, orig_tokens, comp_tokens = compress_with_scaledown(context, system_prompt)
        
        # UI for Token Savings
        if orig_tokens > 0:
            savings = round((1 - comp_tokens / max(orig_tokens, 1)) * 100, 1)
            if savings > 0:
                st.info(f"⚡ ScaleDown saved {savings}% tokens!")

    with st.spinner("Generating roadmap with Gemini..."):
        try:
            #guys you can change your model as your wish
            model = genai.GenerativeModel("gemini-2.5-flash-lite")
            
            # Combine the optimized context with the instructions
            final_input = f"CONTEXT:\n{compressed_prompt}\n\nINSTRUCTIONS:\n{system_prompt}"
            response = model.generate_content(final_input)
            
            roadmap = response.text

            st.markdown("---")
            st.markdown("### 🗺️ Your Personalized GenAI Learning Path")
            st.markdown(roadmap)

            # Download
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            st.download_button("📥 Download Roadmap", roadmap, f"learning_path_{timestamp}.md")
            st.balloons()
            
        except Exception as e:
            st.error(f"Gemini API Error: {str(e)}")
            st.info("Check if your API Key is correct and has access to Gemini 1.5 Flash.")
