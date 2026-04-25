import os
import json
import re
import PyPDF2
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 🔥 MASTER SKILL BANK
# =========================
SKILL_BANK = [
    "python", "java", "c++", "cpp", "javascript",
    "fastapi", "django", "flask", "react", "nodejs",
    "sql", "mysql", "postgresql", "mongodb", "redis",
    "aws", "azure", "gcp",
    "docker", "kubernetes", "ci/cd", "git",
    "tensorflow", "pytorch", "opencv", "nlp",
    "dsa", "system design", "oops", "multithreading",
    "az-900"
]


# =========================
# GROQ CALL
# =========================
def groq_call(prompt, max_tokens=250):
    try:
        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=max_tokens
        )
        return res.choices[0].message.content
    except Exception as e:
        print("Groq error:", e)
        return None


# =========================
# JSON PARSER
# =========================
def extract_json(text):
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        return {}
    return {}


# =========================
# PDF TEXT EXTRACTION
# =========================
def extract_text_from_pdf(path):
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
    return text.lower()


# =========================
# NAME = PDF FILENAME (KEEP SIMPLE - YOUR DECISION)
# =========================
def extract_candidate_name_from_file(file):
    return file.replace(".pdf", "").replace("_", " ").title()


# =========================
# SKILL EXTRACTION (JD)
# =========================
def parse_jd(jd_text):
    prompt = f"""
You are a strict skill extractor.

ONLY choose from:
{SKILL_BANK}

Return JSON:
{{"skills": ["python", "fastapi"]}}

JD:
{jd_text}
"""

    out = groq_call(prompt, max_tokens=200)
    data = extract_json(out)

    return {
        "skills": [s.lower() for s in data.get("skills", []) if s.lower() in SKILL_BANK]
    }


# =========================
# RESUME SKILL EXTRACTION
# =========================
def extract_candidate(text):
    prompt = f"""
Extract skills ONLY from resume.

ONLY use:
{SKILL_BANK}

Return JSON:
{{
  "skills": ["python"],
  "summary": "short summary"
}}

Resume:
{text[:3000]}
"""

    out = groq_call(prompt, max_tokens=250)
    data = extract_json(out)

    skills = [s.lower() for s in data.get("skills", []) if s.lower() in SKILL_BANK]

    return {
        "skills": skills,
        "summary": data.get("summary", "")
    }


# =========================
# LOAD RESUMES
# =========================
def load_resumes():

    base = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(base, "data", "resumes")

    resumes = []

    for file in os.listdir(folder):
        if file.endswith(".pdf"):

            path = os.path.join(folder, file)
            text = extract_text_from_pdf(path)

            profile = extract_candidate(text)

            # 🔥 SIMPLE & RELIABLE NAME SOURCE
            name = extract_candidate_name_from_file(file)

            resumes.append({
                "name": name,
                "file": file,
                "text": text,
                "skills": profile["skills"],
                "summary": profile["summary"]
            })

    return resumes


# =========================
# MATCHING ENGINE
# =========================
def match_candidate(candidate, jd):

    matched = list(set(candidate["skills"]) & set(jd["skills"]))
    missing = list(set(jd["skills"]) - set(candidate["skills"]))

    prompt = f"""
You are a recruiter.

Job: {jd["skills"]}
Candidate: {candidate["skills"]}

Matched: {matched}
Missing: {missing}

Return JSON:
{{
  "score": 0-100,
  "reason": "short reason"
}}
"""

    out = groq_call(prompt, max_tokens=120)
    data = extract_json(out)

    score = data.get("score", len(matched) * 10)

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "reason": data.get("reason", "based on skill overlap")
    }


# =========================
# CHAT GENERATION (FIXED WITH NAME)
# =========================
def generate_chat(candidate, jd_text):

    chat = []

    candidate_name = candidate["name"]

    q1 = groq_call(f"""
Ask ONE technical question based on JD.
Max 15 words.

JD:
{jd_text}
""", max_tokens=80)

    a1 = groq_call(f"""
Answer as candidate.

Resume:
{candidate["text"]}

Question:
{q1}

Answer in 3-4 lines.
""", max_tokens=150)

    chat.append({"role": "recruiter", "message": q1})

    chat.append({
        "role": "candidate",
        "name": candidate_name,
        "message": a1
    })

    q2 = groq_call(f"""
Ask ONE follow-up question based on answer.
Max 15 words.
""", max_tokens=80)

    a2 = groq_call(f"""
Answer as candidate.

Question:
{q2}

Resume:
{candidate["text"]}

Answer in 3-4 lines.
""", max_tokens=150)

    chat.append({"role": "recruiter", "message": q2})

    chat.append({
        "role": "candidate",
        "name": candidate_name,
        "message": a2
    })

    return chat


# =========================
# INTEREST SCORE
# =========================
def evaluate_interest(chat):

    prompt = f"""
Evaluate candidate interest.

Return JSON:
{{
  "interest_score": 0-100,
  "reason": "short reason"
}}

Chat:
{json.dumps(chat)}
"""

    out = groq_call(prompt, max_tokens=120)
    data = extract_json(out)

    return {
        "interest_score": data.get("interest_score", 50),
        "reason": data.get("reason", "neutral")
    }


# =========================
# FINAL SCORE
# =========================
def final_score(m, i):
    return round((0.7 * m) + (0.3 * i), 2)


# =========================
# PIPELINE
# =========================
def run_pipeline(jd_text):

    jd = parse_jd(jd_text)
    resumes = load_resumes()

    results = []

    for c in resumes:

        match = match_candidate(c, jd)
        chat = generate_chat(c, jd_text)
        interest = evaluate_interest(chat)

        results.append({
            "name": c["name"],
            "match_score": match["score"],
            "interest_score": interest["interest_score"],
            "final_score": final_score(match["score"], interest["interest_score"]),
            "matched_skills": match["matched"],
            "missing_skills": match["missing"],
            "reason": match["reason"],
            "chat": chat
        })

    return sorted(results, key=lambda x: x["final_score"], reverse=True)


# =========================
# API
# =========================
@app.post("/analyze")
def analyze(payload: dict):
    jd = payload.get("jd", "")
    return run_pipeline(jd)