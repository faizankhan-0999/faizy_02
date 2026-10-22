# ResumeMatch AI 🎯

ResumeMatch AI is a production-grade, AI-powered resume and job description matching web application built with Streamlit and powered by the official Google GenAI SDK (`gemini-2.5-flash`). It features a modern dark-mode SaaS dashboard designed for precise ATS (Applicant Tracking System) auditing, skill gap identification, and instant candidate optimization.

---

## 🚀 Features

- **📊 ATS Compatibility Scoring**: Evaluates resume suitability against job requirements on a 0–100 scale using visual Plotly donut charts.
- **🔍 Deep Gap Analysis**: Separates fully matched skills from missing requirements and underrepresented experience areas.
- **💡 Actionable Resume Improvements**: Provides targeted bullet-point phrasing suggestions to boost interview conversion rates.
- **🔑 Keyword Optimization**: Recommends high-impact job description keywords to embed into your resume.
- **📥 Executive PDF Reports**: Generates and downloads clean, structured PDF summary reports using ReportLab.
- **🔒 Privacy-First Design**: Processes resumes in-memory without persistent server storage.

---

## 🛠️ Tech Stack

- **Framework**: [Streamlit](https://streamlit.io/) (Python-based UI and deployment runtime)
- **AI Engine**: Google GenAI SDK (`google-genai` with `gemini-2.5-flash`)
- **PDF Extraction**: `pypdf`
- **Visualizations**: `plotly`
- **PDF Generation**: `reportlab`
- **Validation**: `pydantic`

---

## 📁 Project File Structure

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
│   ├── __init__.py
│   ├── gemini_service.py
│   ├── report_generator.py
│   ├── resume_parser.py
│   └── scoring.py
└── tests/
    ├── test_resume_parser.py
    ├── test_scoring.py
    └── test_validation.py
└── app.py
