import asyncio
import streamlit as st

from scanner import scan_source
from package_checker import verify_packages
from remediation import calculate_score
from sanitizer import sanitize_secrets
from models import Finding

# Configure Streamlit Page
st.set_page_config(
    page_title="CodeSanitizer | AI Code Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern AI-assistant theme (Claude / ChatGPT style)
st.markdown("""
<style>
    /* Dark theme background */
    .stApp {
        background-color: #0e1117;
        color: #e6e8eb;
    }
    
    /* Center layout constraint */
    .main .block-container {
        max-width: 900px !important;
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
    }

    /* Custom Header Styling */
    .header-box {
        text-align: center;
        margin-bottom: 2rem;
    }
    .header-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .header-subtitle {
        color: #9ca3af;
        font-size: 0.95rem;
    }

    /* Metric cards styling */
    div[data-testid="stMetric"] {
        background-color: #161922;
        border: 1px solid #262b36;
        padding: 12px 16px;
        border-radius: 8px;
    }

    /* Primary button style */
    .stButton > button {
        width: 100%;
        background-color: #6366f1;
        color: #ffffff;
        border: none;
        padding: 0.6rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        transition: background-color 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #4f46e5;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("""
<div class="header-box">
    <div class="header-title">🛡️ CodeSanitizer</div>
    <div class="header-subtitle">AI Code Security & Package Hallucination Auditor</div>
</div>
""", unsafe_allow_html=True)

default_code = '''import subprocess
import pickle
import fake_ai_package

API_KEY = "sk-example-secret-key"

user_input = input("Enter command: ")
eval(user_input)

subprocess.run(user_input, shell=True)
data = pickle.loads(user_input)
'''

# Input Code Box
code = st.text_area("Paste Python Source Code", value=default_code, height=260)

if st.button("🔍 Scan Code"):
    result = scan_source(code)

    if not result["success"]:
        st.error(f"Python Syntax Error: {result['syntax_error']}")
    else:
        findings = result["findings"]

        # Asynchronously verify external dependencies
        with st.spinner("Analyzing imports on PyPI..."):
            package_results = asyncio.run(verify_packages(result["imports"]))

        # Flag hallucinated non-existent packages
        for pkg in package_results:
            if pkg["exists"] is False:
                findings.append(
                    Finding(
                        severity="High",
                        category="Package Hallucination",
                        message=f"Package '{pkg['package']}' does not exist on PyPI.",
                        remediation="Verify dependency name. AI models often hallucinate non-existent imports."
                    )
                )

        score = calculate_score(findings)

        st.divider()

        # Score & Summary Section
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Security Score", f"{score}/100")
        col2.metric("Critical Issues", sum(f.severity == "Critical" for f in findings))
        col3.metric("High Issues", sum(f.severity == "High" for f in findings))
        col4.metric("Total Findings", len(findings))

        # Tabs for organized view
        tab_findings, tab_deps, tab_sanitized = st.tabs(["🛡️ Security Findings", "📦 Dependencies", "🧹 Sanitized Code"])

        with tab_findings:
            if not findings:
                st.success("No security vulnerabilities detected.")
            else:
                for finding in findings:
                    with st.expander(f"[{finding.severity}] {finding.category}"):
                        if finding.line:
                            st.write(f"**Line:** {finding.line}")
                        st.write(f"**Details:** {finding.message}")
                        if finding.code:
                            st.code(finding.code, language="python")
                        st.info(f"**Remediation:** {finding.remediation}")

        with tab_deps:
            if not package_results:
                st.info("No external imports detected.")
            else:
                for pkg in package_results:
                    if pkg["exists"]:
                        st.success(f"✅ **{pkg['package']}** — Verified on PyPI (v{pkg['version']})")
                    elif pkg["exists"] is False:
                        st.error(f"🚨 **{pkg['package']}** — Non-existent package (Hallucination Risk)")
                    else:
                        st.warning(f"⚠️ **{pkg['package']}** — Status unknown ({pkg['error']})")

        with tab_sanitized:
            sanitized_code, env_example = sanitize_secrets(code)

            if env_example:
                st.warning("Hardcoded secrets detected and extracted into environment variables.")
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    st.download_button("⬇️ Download .env.example", data=env_example, file_name=".env.example", mime="text/plain")
                with col_btn2:
                    st.download_button("⬇️ Download Cleaned Code", data=sanitized_code, file_name="sanitized.py", mime="text/x-python")

                st.code(sanitized_code, language="python")
            else:
                st.info("No hardcoded secrets detected in source code.")