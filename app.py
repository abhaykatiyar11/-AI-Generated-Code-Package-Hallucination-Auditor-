import asyncio
import streamlit as st
from scanner import scan_source, sanitize_secrets
from package_checker import verify_packages

st.set_page_config(page_title="CodeSanitizer", page_icon="🛡️", layout="wide")

st.title("🛡️ CodeSanitizer")
st.caption("AI-Generated Code Security & Package Hallucination Auditor")

default_code = '''import subprocess
import pickle
import fake_ai_package

API_KEY = "sk-example-secret-key"
user_input = input("Enter command: ")
eval(user_input)
'''

code = st.text_area("Paste Python Source Code", value=default_code, height=300)

if st.button("🔍 Scan Code", type="primary"):
    result = scan_source(code)
    
    if not result["success"]:
        st.error(f"Syntax Error: {result['syntax_error']}")
    else:
        with st.spinner("Verifying packages on PyPI..."):
            package_results = asyncio.run(verify_packages(result["imports"]))
            
        # Display Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Security Findings", len(result["findings"]))
        col2.metric("Imports Analyzed", len(result["imports"]))
        col3.metric("Unverified Packages", sum(1 for p in package_results if not p["exists"]))
        
        # Display Findings
        st.subheader("Security Findings")
        for finding in result["findings"]:
            with st.expander(f"[{finding['severity']}] {finding['category']}"):
                st.write(f"**Line:** {finding['line']}")
                st.write(f"**Details:** {finding['message']}")
                st.info(f"**Remediation:** {finding['remediation']}")

        # Display Package Results
        st.subheader("📦 Dependency Analysis")
        for pkg in package_results:
            if pkg["exists"]:
                st.success(f"✅ {pkg['package']} (v{pkg['version']})")
            else:
                st.error(f"🚨 {pkg['package']} — Not found on PyPI")
