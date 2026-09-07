import asyncio
import streamlit as st

from models import Finding
from package_checker import verify_packages
from remediation import calculate_security_score, generate_remediation_summary
from sanitizer import suggest_sanitized_code
from scanner import scan_source
from secret_detector import detect_secrets

st.set_page_config(page_title="CodeSanitizer", page_icon="🛡️", layout="wide")

st.title("🛡️ CodeSanitizer — Python Static Analysis")
st.write("Analyze Python code for security flaws, hardcoded secrets, and dependency supply chain risks.")

# Input area
code_input = st.text_area("Paste Python Code Here:", height=300)

if st.button("Run Security Scan", type="primary"):
    if not code_input.strip():
        st.warning("Please provide code to scan.")
    else:
        # 1. AST Analysis
        ast_results = scan_source(code_input)

        if not ast_results["success"]:
            st.error(f"Syntax Error in input code: {ast_results['syntax_error']}")
        else:
            findings: list[Finding] = ast_results["findings"]

            # 2. Secret Detection
            secrets = detect_secrets(code_input)
            for secret in secrets:
                findings.append(
                    Finding(
                        severity="Critical",
                        category="Hardcoded Secret",
                        message=f"Detected {secret['name']}",
                        line=secret["line"],
                        code=secret["text"],
                        remediation="Move sensitive keys to environment variables or a secret manager.",
                    )
                )

            # 3. Async PyPI Check
            imports = ast_results["imports"]
            package_results = asyncio.run(verify_packages(imports))

            for pkg_info in package_results:
                if pkg_info["exists"] is False:
                    findings.append(
                        Finding(
                            severity="High",
                            category="Dependency Risk",
                            message=f"Imported package '{pkg_info['package']}' was not found on PyPI.",
                            remediation="Verify package spelling to avoid typosquatting attacks.",
                        )
                    )

            # Dashboard Header Metrics
            score = calculate_security_score(findings)
            col1, col2, col3 = st.columns(3)
            col1.metric("Security Health Score", f"{score}/100")
            col2.metric("Total Findings", len(findings))
            col3.metric("Dependencies Checked", len(imports))

            st.divider()

            # Detailed Results
            tab1, tab2, tab3 = st.columns(3)

            st.subheader("🔍 Analysis Findings")
            if not findings:
                st.success("No security issues detected!")
            else:
                for f in findings:
                    with st.expander(f"[{f.severity}] {f.category} — Line {f.line or 'N/A'}"):
                        st.write(f"**Message:** {f.message}")
                        if f.code:
                            st.code(f.code)
                        if f.remediation:
                            st.info(f"**Remediation:** {f.remediation}")

            st.divider()

            # Refactored Code Suggestions
            st.subheader("✨ Suggested Refactored Code")
            sanitized = suggest_sanitized_code(code_input)
            st.code(sanitized, language="python")
