import asyncio
from flask import Flask, render_template_string, request, jsonify

from scanner import scan_source
from package_checker import verify_packages
from remediation import calculate_score
from sanitizer import sanitize_secrets
from models import Finding

app = Flask(__name__)

DEFAULT_CODE = '''import subprocess
import pickle
import fake_ai_package

API_KEY = "sk-example-secret-key"

user_input = input("Enter command: ")
eval(user_input)

subprocess.run(user_input, shell=True)
data = pickle.loads(user_input)
'''

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodeSanitizer | AI Code Security</title>
    <style>
        body {
            background-color: #0e1117;
            color: #e6e8eb;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 2rem;
            display: flex;
            justify-content: center;
        }
        .container {
            max-width: 900px;
            width: 100%;
        }
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
        textarea {
            width: 100%;
            height: 260px;
            background-color: #161922;
            color: #e6e8eb;
            border: 1px solid #262b36;
            border-radius: 8px;
            padding: 12px;
            font-family: monospace;
            font-size: 0.9rem;
            box-sizing: border-box;
            resize: vertical;
        }
        button {
            width: 100%;
            background-color: #6366f1;
            color: #ffffff;
            border: none;
            padding: 0.8rem 1rem;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 1rem;
            transition: background-color 0.2s ease;
        }
        button:hover {
            background-color: #4f46e5;
        }
        .results {
            margin-top: 2rem;
            background: #161922;
            border: 1px solid #262b36;
            padding: 20px;
            border-radius: 8px;
        }
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-bottom: 1.5rem;
        }
        .metric-card {
            background: #0e1117;
            border: 1px solid #262b36;
            padding: 12px;
            border-radius: 6px;
            text-align: center;
        }
        .metric-value {
            font-size: 1.2rem;
            font-weight: bold;
            color: #6366f1;
        }
        .metric-label {
            font-size: 0.8rem;
            color: #9ca3af;
        }
        .finding-item {
            background: #0e1117;
            border-left: 4px solid #ef4444;
            padding: 10px 15px;
            margin-bottom: 10px;
            border-radius: 4px;
        }
        .success-box {
            color: #10b981;
            background: rgba(16, 185, 129, 0.1);
            padding: 10px;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header-box">
            <div class="header-title">🛡️ CodeSanitizer</div>
            <div class="header-subtitle">AI Code Security & Package Hallucination Auditor</div>
        </div>

        <form method="POST">
            <label for="code">Paste Python Source Code</label><br><br>
            <textarea name="code" id="code">{{ code }}</textarea>
            <button type="submit">🔍 Scan Code</button>
        </form>

        {% if evaluated %}
        <div class="results">
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-value">{{ score }}/100</div>
                    <div class="metric-label">Security Score</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{{ critical_count }}</div>
                    <div class="metric-label">Critical Issues</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{{ high_count }}</div>
                    <div class="metric-label">High Issues</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{{ findings|length }}</div>
                    <div class="metric-label">Total Findings</div>
                </div>
            </div>

            <h3>🛡️ Security Findings</h3>
            {% if not findings %}
                <div class="success-box">No security vulnerabilities detected.</div>
            {% else %}
                {% for finding in findings %}
                <div class="finding-item">
                    <strong>[{{ finding.severity }}] {{ finding.category }}</strong><br>
                    <small>{{ finding.message }}</small><br>
                    <em>Remediation: {{ finding.remediation }}</em>
                </div>
                {% endfor %}
            {% endif %}

            <h3>📦 Dependencies</h3>
            {% for pkg in package_results %}
                {% if pkg.exists %}
                    <div style="color: #10b981;">✅ <strong>{{ pkg.package }}</strong> — Verified on PyPI (v{{ pkg.version }})</div>
                {% else %}
                    <div style="color: #ef4444;">🚨 <strong>{{ pkg.package }}</strong> — Non-existent package (Hallucination Risk)</div>
                {% endif %}
            {% endfor %}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    code = DEFAULT_CODE
    evaluated = False
    findings = []
    package_results = []
    score = 100
    critical_count = 0
    high_count = 0

    if request.method == "POST":
        code = request.form.get("code", "")
        evaluated = True
        result = scan_source(code)

        if result["success"]:
            findings = result["findings"]
            package_results = asyncio.run(verify_packages(result["imports"]))

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
            critical_count = sum(1 for f in findings if f.severity == "Critical")
            high_count = sum(1 for f in findings if f.severity == "High")

    return render_template_string(
        HTML_TEMPLATE,
        code=code,
        evaluated=evaluated,
        findings=findings,
        package_results=package_results,
        score=score,
        critical_count=critical_count,
        high_count=high_count
    )

if __name__ == "__main__":
    app.run(debug=True)
