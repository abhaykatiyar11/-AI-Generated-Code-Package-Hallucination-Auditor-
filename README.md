## 🔄 System Flowchart

The following flowchart illustrates the complete CodeSanitizer workflow, from AI-generated Python code input to security analysis, package verification, remediation, sanitization, and deployment.

```mermaid
flowchart TD

    A([Start CodeSanitizer]) --> B[Input Python Code]

    B --> C[Parse Code Using Python AST]

    C --> D{Valid Python Syntax?}

    D -- No --> E[Display Syntax Error]
    E --> Z([End])

    D -- Yes --> F[Traverse AST Using NodeVisitor]

    F --> G{Parallel Security Analysis}

    G --> H[Dangerous Function Detection]
    G --> I[Hardcoded Secret Detection]
    G --> J[Unsafe Deserialization Detection]
    G --> K[Extract Imports & Dependencies]

    K --> L[Normalize Package Names]
    L --> M[Ignore Python Standard Library]
    M --> N[Async PyPI Verification]

    N --> O{Package Exists?}

    O -- Yes --> P[Retrieve Package Version & Metadata]
    O -- No --> Q[Flag Potential Package Hallucination]
    O -- Error/Timeout --> R[Mark Verification Unavailable]

    H --> S[Aggregate Findings]
    I --> S
    J --> S
    P --> S
    Q --> S
    R --> S

    S --> T[Assign Severity]

    T --> U[Critical / High / Medium / Low / Info]

    U --> V[Calculate Security Score]

    V --> W[Generate Remediation Recommendations]

    W --> X{Hardcoded Secret Found?}

    X -- Yes --> Y[Generate Sanitized Code]
    Y --> Y1[Generate .env.example]
    Y --> Y2[Enable Sanitized Code Download]

    X -- No --> AA[Continue]

    Y1 --> AB[Streamlit Security Dashboard]
    Y2 --> AB
    AA --> AB

    AB --> AC[Display Security Score]
    AB --> AD[Display Findings by Severity]
    AB --> AE[Display Package Verification]
    AB --> AF[Display Remediation Advice]

    AC --> AG{Security Threshold Passed?}
    AD --> AG
    AE --> AG
    AF --> AG

    AG -- Yes --> AH[PASS]
    AG -- No --> AI[BLOCK]

    AH --> AJ[Pre-Commit Security Gate]
    AI --> AJ

    AJ --> AK[Push Project to GitHub]

    AK --> AL[GitHub Repository]

    AL --> AM[Connect to Streamlit Community Cloud]

    AM --> AN[Deploy app.py]

    AN --> AO([Live CodeSanitizer Application])
```

### 🛡️ Security Analysis Components

| Component                       | Purpose                                                    |
| ------------------------------- | ---------------------------------------------------------- |
| **Python AST**                  | Parses and understands the actual structure of Python code |
| **Secret Detector**             | Identifies hardcoded API keys, passwords and tokens        |
| **Dangerous Function Detector** | Detects `eval()`, `exec()`, unsafe subprocess usage, etc.  |
| **Deserialization Detector**    | Detects dangerous patterns such as `pickle.loads()`        |
| **Import Extractor**            | Extracts dependencies directly from the AST                |
| **Async PyPI Checker**          | Concurrently verifies external packages against PyPI       |
| **Severity Engine**             | Classifies findings as Critical, High, Medium, Low or Info |
| **Remediation Engine**          | Generates practical fixes                                  |
| **Sanitizer**                   | Replaces detected secrets with environment variables       |
| **`.env.example` Generator**    | Creates a safe environment-variable template               |
| **Security Dashboard**          | Displays the complete scan results                         |
| **Pre-Commit Gate**             | Can block commits containing serious vulnerabilities       |

### 🔐 Overall Security Pipeline

```text
AI-Generated Code
       ↓
Python AST Parsing
       ↓
Structural Analysis
       ↓
┌───────────────┬────────────────┬─────────────────┐
│               │                │                 │
▼               ▼                ▼                 ▼
Secrets      Dangerous       Deserialization   Imports
Detection    Functions        Detection        Extraction
│               │                │                 │
└───────────────┴────────────────┴─────────────────┘
                         ↓
                Async PyPI Verification
                         ↓
              Package Hallucination Check
                         ↓
                 Finding Aggregation
                         ↓
                 Severity Classification
                         ↓
                  Security Score
                         ↓
                 Remediation Advice
                         ↓
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
       Secret Found?              No Secret
             │                       │
             ▼                       │
      Sanitized Code                │
             │                       │
      .env.example                  │
             │                       │
             └───────────┬───────────┘
                         ↓
                 Streamlit Dashboard
                         ↓
                  Security Threshold
                    ↙            ↘
                 PASS            BLOCK
                    ↓              ↓
                    └──────┬───────┘
                           ↓
                    Pre-Commit Gate
                           ↓
                       GitHub
                           ↓
                Streamlit Cloud
                           ↓
                    Live Application
```

## 🚀 Deployment

CodeSanitizer can be developed locally in VS Code, pushed to GitHub, and deployed through Streamlit Community Cloud.

```text
VS Code
   ↓
Local Testing
   ↓
Git Commit
   ↓
Git Push
   ↓
GitHub Repository
   ↓
Streamlit Community Cloud
   ↓
Live CodeSanitizer
```

# 🛡️ CodeSanitizer

AI-Generated Code & Package Hallucination Auditor.

CodeSanitizer detects security problems commonly introduced by AI-generated Python code.

## Features

- AST-based Python security analysis
- Hardcoded secret detection
- Dangerous function detection
- Unsafe deserialization detection
- Command injection detection
- PyPI package verification
- Async dependency checking
- Security score
- Remediation recommendations
- .env.example generation
- Sanitized code download
- Streamlit dashboard
- CLI/pre-commit ready architecture

## Run locally

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run:

streamlit run app.py

## Security Architecture

CodeSanitizer parses Python source code using Python's AST module.

Imports are extracted from the syntax tree and verified against PyPI.

Security findings are assigned severity levels and remediation guidance.


