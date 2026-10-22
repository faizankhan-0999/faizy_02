import streamlit as st
import plotly.graph_objects as go
import os
import io

from src.resume_parser import extract_text_from_pdf
from src.gemini_service import analyze_resume_match
from src.report_generator import generate_pdf_report

# Streamlit Page Config
st.set_page_config(
    page_title="ResumeMatch AI | Premium AI Resume Analysis",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Premium Dark CSS
CUSTOM_CSS = """
<style>
    /* Dark Theme Core Variables */
    :root {
        --bg-main: #0B1020;
        --card-bg: #121A2B;
        --border-color: #253149;
        --text-primary: #F1F5F9;
        --text-muted: #94A3B8;
        --accent-green: #22C55E;
        --accent-purple: #8B5CF6;
        --accent-blue: #38BDF8;
    }
    
    /* Main Background */
    .stApp {
        background-color: var(--bg-main);
        color: var(--text-primary);
    }
    
    /* Hide Default Header/Footer elements */
    header[data-testid="stHeader"] { background: transparent; }
    footer { visibility: hidden; }

    /* Custom Navbar */
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0rem 2rem 0rem;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 2rem;
    }
    .logo-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .badge-ai {
        background: linear-gradient(135deg, var(--accent-purple), var(--accent-blue));
        color: white;
        font-size: 0.75rem;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-weight: 600;
    }

    /* Cards */
    div[data-testid="stForm"], .css-card {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
    }

    /* Badges & Tags */
    .skill-badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 0.2rem;
    }
    .badge-matched {
        background-color: rgba(34, 197, 94, 0.15);
        color: #4ADE80;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }
    .badge-missing {
        background-color: rgba(239, 68, 68, 0.15);
        color: #FCA5A5;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    .badge-keyword {
        background-color: rgba(56, 189, 248, 0.15);
        color: #7DD3FC;
        border: 1px solid rgba(56, 189, 248, 0.3);
    }

    /* Custom Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, var(--accent-purple), #6366F1);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize Session State
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "current_tab" not in st.session_state:
    st.session_state.current_tab = "Dashboard"

# Header Navigation
st.markdown(
    """
    <div class="nav-container">
        <div class="logo-title">
            🎯 ResumeMatch AI <span class="badge-ai">PRO</span>
        </div>
        <div style="color: #94A3B8; font-size: 0.9rem;">
            AI-powered career insights & ATS audit
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Navigation Tabs
tabs = ["Dashboard", "Resume Analysis", "About & Security"]
selected_tab = st.radio("", tabs, horizontal=True, label_visibility="collapsed")

if selected_tab == "About & Security":
    st.title("About ResumeMatch AI")
    st.markdown("""
    ### Privacy & Security First
    - **No Data Retention**: Uploaded resumes are processed in-memory and are never stored on permanent disk storage.
    - **Google GenAI API Processing**: Text content is transmitted securely to Google's Gemini models for processing.
    - **Algorithmic Fairness**: Suitability scores are derived purely from documented skills, work experience, and job requirements.
    - **Disclaimer**: Scores and recommendations provided are automated AI estimations and do not guarantee hiring outcomes.
    """)

elif selected_tab == "Dashboard":
    # Hero Header
    st.markdown("## Find your perfect job match.")
    st.markdown("<p style='color: #94A3B8;'>Upload your resume and paste a target job description to get instant ATS feedback, gap analysis, and tailored keywords.</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Workspace Input
    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        st.markdown("### 1. Upload Resume")
        uploaded_file = st.file_uploader(
            "Upload PDF Resume (Max 5MB)",
            type=["pdf"],
            help="PDF files with selectable text only."
        )
        if uploaded_file:
            st.caption(f"📄 **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")

    with col_right:
        st.markdown("### 2. Job Description")
        job_title = st.text_input("Job Title (Optional)", placeholder="e.g. Senior Full Stack Engineer")
        company = st.text_input("Company Name (Optional)", placeholder="e.g. Acme Corp")
        job_desc = st.text_area(
            "Job Description*",
            height=200,
            placeholder="Paste the full job description or key requirements here...",
            max_chars=8000
        )
        st.caption(f"Character count: {len(job_desc)} / 8000")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Submit Action Button
    analyze_click = st.button("🚀 Analyze Resume Fit", use_container_width=True)

    if analyze_click:
        # Input Validation
        if not uploaded_file:
            st.error("Please upload a valid PDF resume.")
        elif not job_desc.strip():
            st.error("Please enter a job description.")
        else:
            with st.spinner("Extracting text and auditing match with Gemini AI..."):
                # Parse PDF
                resume_text, parse_error = extract_text_from_pdf(uploaded_file)
                if parse_error:
                    st.error(parse_error)
                else:
                    try:
                        # Retrieve Gemini API Key from Streamlit Secrets or Environment
                        api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else os.environ.get("GEMINI_API_KEY")
                        
                        # API Call
                        results = analyze_resume_match(
                            resume_text=resume_text,
                            job_description=job_desc,
                            job_title=job_title,
                            company=company,
                            api_key=api_key
                        )
                        st.session_state.analysis_result = results
                        st.success("Analysis complete!")
                    except Exception as e:
                        st.error(f"Analysis Error: {str(e)}")

    # Display Analysis Results Dashboard
    if st.session_state.analysis_result:
        res = st.session_state.analysis_result
        st.markdown("---")
        st.markdown("## 📊 Analysis Dashboard")

        res_col1, res_col2 = st.columns([1, 2], gap="large")

        with res_col1:
            st.markdown("#### ATS Match Score")
            score = res.get("overall_match_score", 0)

            # Plotly Donut Gauge Chart
            fig = go.Figure(go.Pie(
                values=[score, 100 - score],
                hole=0.75,
                marker_colors=['#8B5CF6', '#253149'],
                textinfo='none',
                hoverinfo='none'
            ))
            fig.update_layout(
                showlegend=False,
                margin=dict(t=10, b=10, l=10, r=10),
                height=220,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                annotations=[dict(
                    text=f"<b>{score}%</b>",
                    x=0.5, y=0.5,
                    font_size=36,
                    font_color='#F1F5F9',
                    showarrow=False
                )]
            )
            st.plotly_chart(fig, use_container_width=True)

            # Executive Summary
            st.markdown("**Executive Summary:**")
            st.info(res.get("summary", ""))

            # PDF Download
            pdf_bytes = generate_pdf_report(res, job_title=job_title, company=company)
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_bytes,
                file_name="ResumeMatch_AI_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        with res_col2:
            # Skill Badges Section
            st.markdown("#### Skills & Qualifications Breakdown")
            
            matched_html = "".join([f'<span class="skill-badge badge-matched">✓ {s}</span>' for s in res.get("matched_skills", [])])
            missing_html = "".join([f'<span class="skill-badge badge-missing">✗ {s}</span>' for s in res.get("missing_skills", [])])
            
            st.markdown("**Matched Skills:**")
            st.markdown(matched_html if matched_html else "_None found_", unsafe_allow_html=True)
            
            st.markdown("<br>**Missing Key Requirements:**", unsafe_allow_html=True)
            st.markdown(missing_html if missing_html else "_None identified_", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Detailed Feedback Tabs
            f_tab1, f_tab2, f_tab3 = st.tabs(["💡 Resume Improvements", "🔑 Recommended Keywords", "🎯 Interview Topics"])
            
            with f_tab1:
                for item in res.get("actionable_improvements", []):
                    st.markdown(f"- {item}")
                    
            with f_tab2:
                kw_html = "".join([f'<span class="skill-badge badge-keyword">{kw}</span>' for kw in res.get("recommended_keywords", [])])
                st.markdown(kw_html, unsafe_allow_html=True)
                
            with f_tab3:
                for topic in res.get("interview_prep_topics", []):
                    st.markdown(f"• {topic}")

        if st.button("🔄 Analyze Another Resume"):
            st.session_state.analysis_result = None
            st.rerun()

# Footer
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; color: #94A3B8; font-size: 0.8rem;'>"
    "ResumeMatch AI • Confidential & Secure • AI compatibility estimates are for guidance purposes only."
    "</div>",
    unsafe_allow_html=True
)
