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










# """
# Tree-sitter Loader for Python Code Parsing
# ------------------------------------------
# Provides functions to initialize and use Tree-sitter
# for extracting code structures like functions, classes, and calls.
# """

# import os
# from tree_sitter import Language, Parser

# BASE_DIR = os.path.dirname(__file__)
# BUILD_DIR = os.path.join(BASE_DIR, "build")
# LANG_SO_PATH = os.path.join(BUILD_DIR, "languages.so")

# def build_language():
#     """
#     Builds the Tree-sitter Python grammar dynamically if not built yet.
#     You need to clone the grammar into:
#     reviewer_core/parsing/tree-sitter-python/
#     """
#     if not os.path.exists(BUILD_DIR):
#         os.makedirs(BUILD_DIR, exist_ok=True)

#     grammar_path = os.path.join(BASE_DIR, "tree-sitter-python")
#     if not os.path.exists(grammar_path):
#         print("⚠️ Tree-sitter Python grammar not found. Clone it using:")
#         print("   git clone https://github.com/tree-sitter/tree-sitter-python.git reviewer_core/parsing/tree-sitter-python")
#         return None

#     print("⚙️ Building Tree-sitter language library...")
#     Language.build_library(LANG_SO_PATH, [grammar_path])
#     print("✅ Tree-sitter Python grammar built successfully.")
#     return LANG_SO_PATH


# def load_parser(language_name: str = "python") -> Parser:
#     """
#     Loads the Tree-sitter parser for Python.
#     Builds the language library if missing.
#     """
#     if not os.path.exists(LANG_SO_PATH):
#         built = build_language()
#         if not built:
#             raise RuntimeError("Tree-sitter Python grammar missing. Build failed.")

#     language = Language(LANG_SO_PATH, language_name)
#     parser = Parser()
#     parser.set_language(language)
#     return parser


# def parse_code(code: str):
#     """
#     Parse Python code into a syntax tree.
#     Returns a Tree-sitter tree object.
#     """
#     parser = load_parser()
#     tree = parser.parse(bytes(code, "utf8"))
#     return tree
