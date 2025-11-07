"""
Bad Example File
----------------
This file intentionally contains style issues,
security risks, and complexity problems
to demonstrate the multi-agent review system.
"""

import os, hashlib, subprocess, pickle, yaml

AKIAZZZZZZZZZZZZZZZZ = "AKIAEXAMPLEKEY1234"  # Hardcoded secret (SEC009)

def BadFunctionName(x, y=[]):  # Non-snake_case + mutable default arg (S101 + S104)
    name = input("Enter your name: ")  # Source of taint
    os.system("echo " + name)  # Command injection (SEC003 + taint)
    eval("print('hi')")  # Dangerous eval (SEC001)
    print(hashlib.md5(b'password').hexdigest())  # Weak hash (SEC007)
    yaml.load("a: 1")  # Unsafe YAML (SEC008)
    data = pickle.loads(b"malicious")  # Insecure deserialization (SEC006)
    return x + y

# Overly complex nested code (to test cyclomatic complexity)
def complicated(a, b, c, d, e, f, g, h, i, j, k):
    for x in range(10):
        if x % 2 == 0:
            if x > 5:
                if x < 8:
                    if a and b:
                        if c and d:
                            if e and f:
                                if g and h:
                                    if i and j:
                                        print(x)
    return 42
