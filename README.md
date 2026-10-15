# 📄 ATS Resume Checker

A Streamlit app that scores a resume for Applicant Tracking Systems (ATS) and tells you exactly how to improve it, powered by Google's Gemini Flash models.

## Features

- Upload a resume as **PDF, DOCX or TXT** (max 5 MB)
- Optional **job description** for a role-specific score and keyword gaps
- Overall **ATS score (0-100)** plus a 5-category breakdown
- Prioritised **improvements** (High / Medium / Low), strengths, missing keywords and formatting issues
- **Before / after rewrite examples** for weak bullet points
- Quick local checks: email, phone, LinkedIn/GitHub, standard sections, word count
- Download the full report as JSON

## Project structure

```
.
├── app.py             # Streamlit app
├── requirements.txt   # Python dependencies
└── README.md
```

## Run locally

1. Get a free Gemini API key from https://aistudio.google.com/apikey
2. Install and run:

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# provide the key (pick ONE)
export GEMINI_API_KEY="your-key"            # Windows PowerShell: $env:GEMINI_API_KEY="your-key"
# or create .streamlit/secrets.toml containing:  GEMINI_API_KEY = "your-key"
# or just paste it into the sidebar when the app opens

streamlit run app.py
```

The app opens at http://localhost:8501.

## Choosing the Gemini model

The default is `gemini-flash-latest`. You can change it in the sidebar, or set the `GEMINI_MODEL` environment variable. If the chosen model is unavailable for your key, the app automatically tries the fallbacks listed in `FALLBACK_MODELS` at the top of `app.py`. Check https://ai.google.dev/gemini-api/docs/models for current model names.

## Deploy on Streamlit Community Cloud

1. Push this repo to GitHub (never commit your API key).
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **Create app**, choose your repo, branch `main`, and main file `app.py`.
4. Open **Advanced settings → Secrets** and add:

   ```toml
   GEMINI_API_KEY = "your-key"
   ```

5. Click **Deploy**.

## Privacy

Resume text is sent to the Gemini API for analysis. The app does not store resumes or reports on a server.

## Limitations

- Scanned/image-only resumes cannot be read (an ATS can't read them either), so export a text-based PDF or DOCX.
- The score is an AI estimate, not the output of any specific employer's ATS. Use it as guidance.
