# ResumeMatch AI 🎯

ResumeMatch AI is a production-grade, AI-powered resume and job description matching application built with Streamlit and Google's official Gemini SDK (`google-genai`). It features a modern dark SaaS dashboard interface designed to evaluate candidate qualifications objectively and deliver actionable ATS insights.

---

## 🚀 Key Features

- **Modern Dark SaaS Dashboard**: Deep navy background (`#0B1020`), clean card layout, glowing accent highlights, responsive components, and custom CSS styling.
- **Gemini-Powered Intelligence**: Uses `gemini-2.5-flash` with strict JSON schema response validation for accurate parsing.
- **ATS Match Score & Breakdown**: Circular gauge score (0–100), matched vs. missing skills analysis, and tailored recommendations.
- **Interactive UI**: Upload PDF resumes, inspect keyword optimization, review interview preparation guidance, and generate PDF export reports.
- **Privacy First**: Temporary in-memory processing with no permanent storage of user resumes or sensitive details.

---

## 🛠️ Tech Stack

- **Framework**: [Streamlit](https://streamlit.io/)
- **AI Core**: [Google GenAI Python SDK (`google-genai`)](https://pypi.org/project/google-genai/) via `gemini-2.5-flash`
- **PDF Extraction**: `pypdf`
- **Visualizations**: `plotly`
- **Reporting**: `reportlab` (PDF report exports)
- **Validation**: `pydantic`

---

## 📂 Project Structure

```text
ai-resume-job-matcher/
├── .gitignore
├── README.md
├── requirements.txt
├── assets/
│   └── logo.svg
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
├── src/
│   /__init__.py
│   ├── gemini_service.py
│   ├── report_generator.py
│   ├── resume_parser.py
│   └── scoring.py
├── tests/
│   ├── test_resume_parser.py
│   ├── test_scoring.py
│   └── test_validation.py
└── app.py
