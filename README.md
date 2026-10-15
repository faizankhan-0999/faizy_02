Resume ATS Checker
A beginner-friendly Streamlit app that extracts resume text and uses Google's Gemini Flash model to provide an estimated ATS-style score, job-description alignment, and practical improvements.
Important: This is an AI estimate, not a score from a real Applicant Tracking System. ATS products differ, and no score guarantees an interview.

Features
- Upload PDF, DOCX, or TXT resumes
- Optional target job description for a more relevant review
- Estimated score with explanations, strengths, potential parsing issues, and keyword alignment
- Prioritized suggestions and example bullet rewrites
- Download the review as Markdown
- API key loaded from Streamlit secrets or an environment variable
1. Requirements
- Python 3.10 or newer
- A Gemini API key from Google AI Studio
- The packages listed in requirements.txt
2. Run locally
Open a terminal in this project folder and create a virtual environment:
Windows
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Create this file: .streamlit/secrets.toml
GEMINI_API_KEY = "paste_your_real_api_key_here"
Then run:
streamlit run app.py
Streamlit will print a local URL, usually http://localhost:8501.
Never commit your API key. Add .streamlit/secrets.toml to .gitignore before pushing to GitHub.
3. Push to GitHub
Create a new empty repository on GitHub, then run these commands in the project folder (replace the URL with your repository URL):
git init
git add app.py README.md requirements.txt .gitignore
git commit -m "Create resume ATS checker"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
If Git asks you to authenticate, follow GitHub's current sign-in instructions. Do not put API keys in Git commands or source files.
Create a .gitignore file containing:
.venv/
__pycache__/
*.py[cod]
.streamlit/secrets.toml
.env
4. Deploy on Streamlit Community Cloud
1. Push the project to GitHub.
2. Open Streamlit Community Cloud and sign in with GitHub.
3. Choose Create app and select your repository, branch (main), and main file path (app.py).
4. Open Advanced settings and add this in the Secrets field:
   GEMINI_API_KEY = "paste_your_real_api_key_here"
5. Deploy the app and wait for the build to finish. Streamlit will provide a public app URL.
Keep the secret in Streamlit's Secrets settings, not in the GitHub repository. If you update dependencies later, the app may take a few minutes to rebuild.
Troubleshooting
- Missing API key: Check the spelling GEMINI_API_KEY and restart the local app after changing secrets.
- Quota/API error: Check your Google AI Studio project, key, model availability, and quota.
- No text extracted: A scanned/image-only PDF may need OCR before upload.
- Import error: Activate your virtual environment and run pip install -r requirements.txt.
- Deployment failure: Review the app logs in Streamlit Community Cloud.
Privacy and responsible use
Resume text is sent to Google Gemini to produce the review. Do not upload personal information unless you are comfortable with that processing. The demo does not intentionally store uploaded resumes in a database. The result is advisory; users should verify all suggestions and never add skills or achievements
