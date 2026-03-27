# 🚀 Notevera AI — Smart AI Learning Assistant

> Transform scattered study material into structured knowledge with AI-generated notes, study plans, oral exam practice, and more.

---

## 🎯 Project Overview

**Notevera AI** is a futuristic, AI-powered student learning platform built for hackathon-speed development with a real startup design philosophy.

**Tech Stack:**

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14 (App Router) + TailwindCSS + Framer Motion |
| Backend | Python FastAPI |
| Database | MongoDB (via Motor async driver) |
| AI | OpenAI GPT-4 / Gemini API |
| Auth | JWT + Google OAuth |
| OCR | Tesseract / Google Vision API |
| PDF | PyMuPDF (fitz) |
| YouTube | youtube-transcript-api + YouTube Data API v3 |

---

## 📁 Folder Structure

```
notevera-ai/
├── backend/
│   ├── app.py                   # FastAPI entry point
│   ├── database.py              # MongoDB connection
│   ├── requirements.txt
│   ├── .env.example
│   ├── routes/
│   │   ├── auth.py              # POST /api/auth/register, /login, /google
│   │   ├── upload.py            # POST /api/upload/
│   │   ├── notes.py             # POST /api/notes/generate
│   │   ├── planner.py           # POST /api/planner/generate
│   │   ├── oral_exam.py         # POST /api/oral-exam/questions, /evaluate
│   │   ├── profile.py           # GET/PUT /api/profile
│   │   ├── settings.py          # GET/PUT /api/settings
│   │   └── export.py            # GET /api/export/pdf/{notes_id}
│   ├── services/
│   │   ├── ai_notes_generator.py
│   │   ├── youtube_recommender.py
│   │   ├── study_planner.py
│   │   └── quiz_generator.py
│   ├── utils/
│   │   ├── ocr_processor.py
│   │   ├── pdf_parser.py
│   │   └── youtube_transcript.py
│   └── models/
│       ├── user.py
│       ├── material.py
│       ├── notes.py
│       └── study_plan.py
│
└── frontend/
    ├── app/
    │   ├── page.tsx              # Landing page
    │   ├── layout.tsx
    │   ├── globals.css
    │   ├── auth/page.tsx         # Login / Signup
    │   ├── dashboard/page.tsx
    │   ├── upload/page.tsx
    │   ├── notes/page.tsx
    │   ├── planner/page.tsx
    │   ├── oral-exam/page.tsx
    │   ├── profile/page.tsx
    │   └── settings/page.tsx
    ├── components/
    │   ├── Navbar.tsx
    │   ├── Sidebar.tsx
    │   ├── GlowCard.tsx
    │   └── StarField.tsx
    ├── context/
    │   └── AuthContext.tsx
    ├── lib/
    │   └── api.ts
    ├── tailwind.config.js
    └── package.json
```

---

## ⚙️ Backend Setup (FastAPI)

### 1. Create Virtual Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Fill in your keys in .env
```

**Required env vars:**
```
MONGODB_URL=mongodb://localhost:27017
JWT_SECRET=your-super-secret-key-change-this
OPENAI_API_KEY=sk-...
YOUTUBE_API_KEY=AIza...
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
```

### 4. Run Backend
```bash
python app.py
# or
uvicorn app:app --reload --port 8000
```

API docs available at: `http://localhost:8000/docs`

---

## 🎨 Frontend Setup (Next.js)

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Configure Environment
```bash
cp .env.example .env.local
# Set NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Run Frontend
```bash
npm run dev
```

Open: `http://localhost:3000`

---

## 🔑 API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Create account |
| POST | `/api/auth/login` | Login with JWT |
| POST | `/api/auth/google` | Google OAuth |
| POST | `/api/upload/` | Upload PDF / image / text / YouTube |
| POST | `/api/notes/generate` | Generate AI notes |
| GET | `/api/notes/` | List user's notes |
| POST | `/api/planner/generate` | Generate study plan |
| GET | `/api/planner/` | Get saved plans |
| POST | `/api/oral-exam/questions` | Generate exam Qs |
| POST | `/api/oral-exam/evaluate` | Evaluate spoken answer |
| GET | `/api/profile` | Get profile data |
| PUT | `/api/settings` | Update preferences |
| GET | `/api/export/pdf/{notes_id}` | Download notes as PDF |

---

## 🤖 AI Prompt Templates

### Notes Generator
```
You are an expert academic tutor. Given the following study material, generate structured notes with:
- Topic Title
- 3-5 Key Concepts (with brief definitions)
- Bullet-point summaries for each concept
- Important formulas or dates (if any)
- A short revision checklist

Material:
{extracted_text}
```

### Question Generator (Oral Exam)
```
Generate 5 oral exam questions for a student based on the following notes.
Make questions progressively harder (recall → application → analysis).
Return as a JSON array: [{"question": "...", "expected_keywords": [...]}]

Notes:
{notes_text}
```

### Answer Evaluator
```
A student answered an oral exam question. Evaluate their answer.

Question: {question}
Expected key concepts: {expected_keywords}
Student's answer: {student_answer}

Return JSON: {"score": 0-100, "feedback": "...", "missing_points": [...]}
```

---

## 🗄️ Database Schema (MongoDB)

### Users Collection
```json
{
  "_id": "ObjectId",
  "name": "string",
  "email": "string (unique)",
  "password_hash": "string",
  "avatar": "string | null",
  "google_id": "string | null",
  "preferences": { "theme": "dark", "gcal_sync": false },
  "created_at": "datetime"
}
```

### Materials Collection
```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId ref",
  "type": "pdf | image | text | youtube",
  "original_name": "string",
  "extracted_text": "string",
  "created_at": "datetime"
}
```

### Notes Collection
```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId ref",
  "material_id": "ObjectId ref",
  "title": "string",
  "content": { "key_concepts": [], "summary": "", "formulas": [] },
  "recommended_lectures": [{ "title": "", "url": "", "thumbnail": "" }],
  "created_at": "datetime"
}
```

### StudyPlans Collection
```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId ref",
  "notes_id": "ObjectId ref",
  "exam_date": "datetime",
  "tasks": [{ "title": "", "type": "", "due_date": "", "completed": false }],
  "gcal_event_ids": [],
  "created_at": "datetime"
}
```

---

## ✨ UI Features

| Feature | Detail |
|---------|--------|
| Theme | Space / galaxy dark with neon purple-blue gradients |
| Animations | Framer Motion page transitions + hover effects |
| Background | Animated star field canvas |
| Cards | Glassmorphism with glowing borders |
| Typography | Orbitron (headings) + Inter (body) |
| Mode Switch | Dark ↔ Light via CSS variables |

---

## 🚀 Future Features (Startup Roadmap)

- [ ] **Team / Group Study** — shared notes and collaborative study rooms
- [ ] **Flashcard Generator** — auto-create spaced repetition flashcards from notes
- [ ] **Progress Analytics** — weekly learning heatmaps and performance graphs
- [ ] **Mobile App** — React Native companion with offline mode
- [ ] **Multi-language Support** — notes in 20+ languages
- [ ] **LMS Integration** — Canvas, Moodle, Google Classroom connectors
- [ ] **AI Tutor Chat** — real-time Q&A on uploaded material
- [ ] **Browser Extension** — clip web articles directly into Notevera
- [ ] **Subscription Tier** — freemium with premium AI features

---

## 👥 Team

Built with ❤️ for hackathon development. Designed to scale into a real startup.

---

*Notevera AI — Study Smarter. Not Harder.* 🌌
