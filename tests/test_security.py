"""
Test — Security Agent
---------------------
Verifies that the security scanner and taint analysis
correctly identify unsafe patterns and risky data flows.
"""

from reviewer_core.security.runner import run_security


def test_detects_eval_usage():
    code = "eval('print(1)')\n"
    findings = run_security("test_eval.py", code)
    assert any(f.rule_id == "SEC001" for f in findings), "Should detect eval() usage"


def test_detects_os_system():
    code = "import os\nos.system('ls')\n"
    findings = run_security("test_os_system.py", code)
    assert any(f.rule_id == "SEC003" for f in findings), "Should detect os.system() usage"


def test_detects_pickle_loads():
    code = "import pickle\npickle.loads(b'data')\n"
    findings = run_security("test_pickle.py", code)
    assert any(f.rule_id == "SEC006" for f in findings), "Should detect pickle.loads() usage"


def test_detects_sql_injection_pattern():
    code = "cursor.execute(f'SELECT * FROM users WHERE name = {user}')\n"
    findings = run_security("test_sql_injection.py", code)
    assert any(f.rule_id == "SEC005" for f in findings), "Should flag raw SQL pattern"


def test_detects_taint_flow():
    code = '''
import os
name = input("Enter name: ")
os.system("echo " + name)
'''
    findings = run_security("test_taint_flow.py", code)
    assert any(f.rule_id == "SEC_T002" for f in findings), "Should detect tainted variable flowing into os.system"
