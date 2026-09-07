import ast
from models import Finding

DANGEROUS_FUNCTIONS = {
    "eval": ("High", "eval() executes dynamically supplied Python code.", "Avoid eval(). Use explicit parsing or safer data formats."),
    "exec": ("Critical", "exec() can execute arbitrary Python code.", "Remove exec() and use explicit program logic."),
    "compile": ("Medium", "compile() generates executable code dynamically.", "Avoid compiling untrusted string input."),
    "__import__": ("Medium", "Dynamic imports can load hidden dependencies.", "Use explicit import statements at module top-level.")
}


class SecurityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.findings = []
        self.imports = []

    def visit_Import(self, node):
        for alias in node.names:
            package = alias.name.split(".")[0]
            self.imports.append(package)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            package = node.module.split(".")[0]
            self.imports.append(package)
        self.generic_visit(node)

    def visit_Call(self, node):
        func_name = None
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr

        if func_name in DANGEROUS_FUNCTIONS:
            severity, message, remediation = DANGEROUS_FUNCTIONS[func_name]
            self.findings.append(
                Finding(
                    severity=severity,
                    category="Dangerous Function",
                    message=message,
                    line=node.lineno,
                    column=node.col_offset,
                    code=func_name,
                    remediation=remediation
                )
            )

        self._check_subprocess(node)
        self._check_yaml(node)
        self._check_pickle(node)
        self.generic_visit(node)

    def _check_subprocess(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr == "run":
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess":
                for kw in node.keywords:
                    if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                        self.findings.append(
                            Finding(
                                severity="High",
                                category="Command Injection",
                                message="subprocess.run(..., shell=True) enables command injection risks.",
                                line=node.lineno,
                                column=node.col_offset,
                                code="shell=True",
                                remediation="Disable shell=True and pass commands as explicit lists of arguments."
                            )
                        )

    def _check_yaml(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr == "load":
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "yaml":
                self.findings.append(
                    Finding(
                        severity="High",
                        category="Unsafe Deserialization",
                        message="yaml.load() can instantiate unsafe arbitrary Python objects.",
                        line=node.lineno,
                        column=node.col_offset,
                        code="yaml.load",
                        remediation="Use yaml.safe_load() when parsing untrusted input."
                    )
                )

    def _check_pickle(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr == "loads":
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "pickle":
                self.findings.append(
                    Finding(
                        severity="Critical",
                        category="Unsafe Deserialization",
                        message="pickle.loads() allows arbitrary remote code execution.",
                        line=node.lineno,
                        column=node.col_offset,
                        code="pickle.loads",
                        remediation="Avoid pickle for untrusted network input. Use standard JSON or Protocol Buffers."
                    )
                )


def scan_source(source: str) -> dict:
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return {
            "success": False,
            "syntax_error": str(exc),
            "findings": [],
            "imports": []
        }

    visitor = SecurityVisitor()
    visitor.visit(tree)

    return {
        "success": True,
        "syntax_error": None,
        "findings": visitor.findings,
        "imports": sorted(set(visitor.imports))
    }
