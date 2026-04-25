# ֎ TALENT GENIE - AI Talent Scouting Agent
<p align="center">
  <img src="./frontend/src/assets/ai-agent.jpeg" width="220"/>
</p>
An AI-powered recruitment assistant that analyzes resumes, ranks candidates, and simulates real interview conversations — all in seconds.

---

## 🚀 Problem

Recruiters spend hours:

* Manually screening resumes
* Matching skills with job descriptions
* Conducting repetitive initial interviews

This process is slow, inefficient, and hard to scale.

---

## 💡 Solution

**AI Talent Agent** automates the entire pipeline:

✅ Parses resumes automatically
✅ Extracts and matches skills with Job Description
✅ Ranks candidates using AI scoring
✅ Simulates recruiter–candidate conversations
✅ Provides explainable hiring insights

---

## ✨ Key Features

### 📄 Resume Parsing

* Extracts text from PDF resumes
* Identifies relevant skills using controlled AI prompts

### 🎯 Smart Skill Matching

* Matches candidate skills with JD
* Identifies missing skills
* Generates match score

### 💬 AI Interview Simulation

* Generates technical questions
* Simulates candidate answers
* Displays structured chat UI

### 📊 Candidate Ranking

* Combines:

  * Match Score (70%)
  * Interest Score (30%)
* Outputs ranked candidate list

---

## 🧠 Tech Stack

### 🔹 Backend

* Python 3.13
* FastAPI
* Groq API (LLaMA 3.1)
* PyPDF2

### 🔹 Frontend

* React (Vite)
* Axios
* Custom UI with chat modal

---

## 🏗️ Architecture Overview

```id="arch1"
User Input (JD)
      ↓
Skill Extraction (LLM)
      ↓
Resume Parsing (PDF)
      ↓
Skill Matching Engine
      ↓
AI Interview Simulation
      ↓
Final Ranking Output
```

---

## ⚙️ Installation

### 🔹 Prerequisites

* Python 3.13+
* Node.js & npm
* Groq API key

---

### 🔹 Backend Setup

```bash id="b1"
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file:

```id="env1"
GROQ_API_KEY=your_api_key_here
```

Run server:

```bash id="b2"
uvicorn main:app --reload --port 8001
```

---

### 🔹 Frontend Setup

```bash id="f1"
cd frontend
npm install
npm run dev
```

---

## 🧪 How It Works

1. Enter Job Description
2. Click **Analyze Candidates**
3. System:

   * Extracts skills
   * Matches resumes
   * Generates interview chats
4. View ranked candidates
5. Open chat to see AI interview

---

## 📊 Sample API

### POST `/analyze`

```json id="api_req"
{
  "jd": "Looking for a Python backend developer"
}
```

### Response

```json id="api_res"
[
  {
    "name": "Chirag Sharma",
    "final_score": 85,
    "match_score": 100,
    "interest_score": 50,
    "matched_skills": ["python", "fastapi"],
    "missing_skills": [],
    "reason": "Strong match for backend role"
  }
]
```

---

## 📂 Project Structure

```id="struct1"
talent-agent/
├── backend/
│   ├── main.py
│   ├── data/resumes/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── assets/
│
└── README.md
```

---

## 🚀 Future Improvements

* 📊 Skill gap visualization dashboard
* 🏆 Top candidate highlight
* 💬 Real-time streaming chat
* 📄 Resume preview in UI
* 🔍 Advanced filtering

---

## 👩‍💻 Author

**Khushi Priya Srivastava**

---

## 🏆 Why This Project Stands Out

* End-to-end AI recruitment pipeline
* Combines NLP + ranking + chat simulation
* Clean UI with real interview experience
* Scalable and production-ready architecture

---

## 📌 Notes

* Resumes should be placed in `backend/data/resumes/`
* Candidate names are derived from PDF filenames
* Ensure backend is running before frontend

---

## ⭐ Impact

Reduces recruiter effort from **hours → seconds**
and enables faster, smarter hiring decisions using AI.

## 📸 Demo Screens

### 🏠 Home Page
<p align="center">
  <img src="./screenshots/SS1.jpeg" width="200"/>
</p>

### 💬 Chat Interface
<p align="center">
  <img src="./screenshots/SS2.jpeg" width="200"/>
</p>

### 📊 Results
<p align="center">
  <img src="./screenshots/SS3.jpeg" width="200"/>
</p>
