"""
Test — Static Analysis
----------------------
Verifies that the static analysis agent correctly detects
style and complexity issues in Python code.
"""

from reviewer_core.static_analysis.runner import run_static


def test_line_length():
    code = 'x = "a" * 120\n'
    findings = run_static("test_line_length.py", code)
    assert any(f.rule_id == "S100" for f in findings), "Should flag long lines"


def test_function_name():
    code = "def BadName():\n    pass\n"
    findings = run_static("test_func_name.py", code)
    assert any(f.rule_id == "S101" for f in findings), "Should flag non-snake_case function names"


def test_mutable_default():
    code = "def foo(x=[]):\n    return x\n"
    findings = run_static("test_mutable_default.py", code)
    assert any(f.rule_id == "S104" for f in findings), "Should flag mutable default argument"


def test_bare_except():
    code = "try:\n    1/0\nexcept:\n    pass\n"
    findings = run_static("test_bare_except.py", code)
    assert any(f.rule_id == "S105" for f in findings), "Should flag bare except clause"


def test_function_length_and_complexity():
    code = "def big():\n" + "    pass\n" * 70
    findings = run_static("test_function_length.py", code)
    assert any(f.rule_id == "C201" for f in findings), "Should flag long function"
