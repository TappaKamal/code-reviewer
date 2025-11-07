"""
Tree-sitter Loader
------------------
This module initializes Tree-sitter for Python parsing.
It automatically clones the grammar if missing, builds it once,
and exposes a helper to parse Python source code into an AST.
"""

import subprocess
from pathlib import Path
from tree_sitter import Language, Parser

# Paths
BASE_DIR = Path(__file__).resolve().parent
LIB_PATH = BASE_DIR / "build.so"
VENDOR_DIR = BASE_DIR.parent.parent / "vendor"
PY_LANG_DIR = VENDOR_DIR / "tree-sitter-python"

# Ensure vendor folder exists
VENDOR_DIR.mkdir(parents=True, exist_ok=True)

# Step 1: Clone tree-sitter-python grammar if not present
if not PY_LANG_DIR.exists():
    print("📦 Cloning tree-sitter-python grammar...")
    subprocess.run(
        ["git", "clone", "https://github.com/tree-sitter/tree-sitter-python", str(PY_LANG_DIR)],
        check=True
    )

# Step 2: Build a language library if not built yet
if not LIB_PATH.exists():
    print("🔨 Building Tree-sitter language library...")
    Language.build_library(
        str(LIB_PATH),
        [str(PY_LANG_DIR)]
    )

# Step 3: Load Python language
PY_LANGUAGE = Language(str(LIB_PATH), "python")

# Step 4: Initialize parser
_parser = Parser()
_parser.set_language(PY_LANGUAGE)

def parse_python(code: str):
    """
    Parse Python code into a Tree-sitter syntax tree.

    Args:
        code (str): Python source code.
    Returns:
        tree (tree_sitter.Tree): The parsed syntax tree.
    """
    if not isinstance(code, bytes):
        code = code.encode("utf-8")
    return _parser.parse(code)
