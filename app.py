import asyncio
import streamlit as st

from scanner import scan_source
from package_checker import verify_packages
from remediation import calculate_score
from sanitizer import sanitize_secrets
from models import Finding

st.set_page_config(page_title="CodeSanitizer", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .main-title { font-size: 38px; font-weight: 800; margin-bottom: 0; }
    .subtitle { font-size: 16px; opacity: 0.75; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🛡️ CodeSanitizer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI Code Security & Package Hallucination Auditor</div>', unsafe_allow_html=True)

default_code = '''import subprocess
import pickle
import fake_ai_package

API_KEY = "sk-example-secret-key"

user_input = input("Enter command: ")
eval(user_input)

subprocess.run(user_input, shell=True)
data = pickle.loads(user_input)
'''

code = st.text_area("Paste Python Source Code", value=default_code, height=300)

if st.button("🔍 Scan Code", type="primary"):
    result = scan_source(code)

    if not result["success"]:
        st.error(f"Python Syntax Error: {result['syntax_error']}")
    else:
        findings = result["findings"]

        with st.spinner("Analyzing packages on PyPI..."):
            package_results = asyncio.run(verify_packages(result["imports"]))

        for pkg in package_results:
            if pkg["exists"] is False:
                findings.append(
                    Finding(
                        severity="High",
                        category="Package Hallucination",
                        message=f"Package '{pkg['package']}' does not exist on PyPI.",
                        remediation="Verify the dependency name. AI models often hallucinate non-existent imports."
                    )
                )

        score = calculate_score(findings)

        st.divider()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Security Score", f"{score}/100")
        col2.metric("Critical", sum(f.severity == "Critical" for f in findings))
        col3.metric("High", sum(f.severity == "High" for f in findings))
        col4.metric("Total Issues", len(findings))

        st.subheader("Security Findings")
        if not findings:
            st.success("No security issues detected.")
        else:
            for finding in findings:
                with st.expander(f"[{finding.severity}] {finding.category}"):
                    if finding.line:
                        st.write(f"**Line:** {finding.line}")
                    st.write(f"**Issue:** {finding.message}")
                    if finding.code:
                        st.code(finding.code, language="python")
                    st.info(f"**Fix:** {finding.remediation}")

        st.subheader("📦 Dependency Analysis")
        for pkg in package_results:
            if pkg["exists"]:
                st.success(f"✅ {pkg['package']} — PyPI version {pkg['version']}")
            elif pkg["exists"] is False:
                st.error(f"🚨 {pkg['package']} — Not found on PyPI")
            else:
                st.warning(f"⚠️ {pkg['package']} — {pkg['error']}")

        st.subheader("🧹 Sanitized Output")
        sanitized_code, env_example = sanitize_secrets(code)

        if env_example:
            st.warning("Hardcoded secrets detected and converted to environment variables.")
            st.download_button("⬇️ Download .env.example", data=env_example, file_name=".env.example", mime="text/plain")
            st.download_button("⬇️ Download Sanitized Code", data=sanitized_code, file_name="sanitized.py", mime="text/x-python")
            st.code(sanitized_code, language="python")
        else:
            st.info("No secrets requiring sanitization were detected.")
