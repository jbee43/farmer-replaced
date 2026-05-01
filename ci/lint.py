#!/usr/bin/env python3
"""Linter for The Farmer Was Replaced game scripts.

Validates module conventions defined in CLAUDE.md:
- Syntax: all .py files must parse without errors
- Core modules (nav, water, sow): function-only, no top-level execution
- Farm modules (farm_*): expose once() and loop(), no top-level execution
- Fun modules (fun_*): expose once() and loop(), no top-level execution
- Quest modules (quest_*): self-contained, no imports
- Global: no 'import move' (shadows the builtin)
- README sync: every script must appear in the Modules table and vice-versa
"""

import ast
import glob
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE_MODULES = {"nav", "water", "sow"}
SKIP_CONVENTIONS = {"__builtins__"}

ALLOWED_TOP_LEVEL = (ast.FunctionDef, ast.Import, ast.ImportFrom)


def classify(filepath):
    name = os.path.splitext(os.path.basename(filepath))[0]
    if name in SKIP_CONVENTIONS:
        return None
    if name in CORE_MODULES:
        return "core"
    if name.startswith("farm_"):
        return "farm"
    if name.startswith("quest_"):
        return "quest"
    if name.startswith("fun_"):
        return "fun"
    return "unknown"


def is_docstring(node):
    return isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)


def check_syntax(py_files):
    """Parse all .py files and return syntax errors."""
    errors = []
    for filepath in py_files:
        relpath = os.path.relpath(filepath, REPO_ROOT)
        with open(filepath, encoding="utf-8") as f:
            source = f.read()
        try:
            ast.parse(source, filename=relpath)
        except SyntaxError as e:
            errors.append(f"{relpath}:{e.lineno}: syntax error: {e.msg}")
    return errors


def check_conventions(py_files):
    """Validate module conventions on classified files."""
    errors = []
    for filepath in py_files:
        relpath = os.path.relpath(filepath, REPO_ROOT)
        kind = classify(filepath)
        if kind is None:
            continue

        with open(filepath, encoding="utf-8") as f:
            source = f.read()

        try:
            tree = ast.parse(source, filename=relpath)
        except SyntaxError:
            continue

        for node in tree.body:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "move":
                        errors.append(f"{relpath}:{node.lineno}: 'import move' shadows the builtin move() function")

        if kind in ("core", "farm", "fun"):
            for node in tree.body:
                if isinstance(node, ALLOWED_TOP_LEVEL) or is_docstring(node):
                    continue
                errors.append(f"{relpath}:{node.lineno}: top-level execution not allowed in {kind} modules")
                break

        if kind in ("farm", "fun"):
            top_funcs = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
            for required in ("once", "loop"):
                if required not in top_funcs:
                    errors.append(f"{relpath}: missing required function {required}()")

        if kind == "quest":
            for node in tree.body:
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    errors.append(f"{relpath}:{node.lineno}: quest modules must be self-contained (no imports)")
                    break

    return errors


def check_readme_sync(py_files):
    """Verify every script has a README table row and vice-versa."""
    errors = []
    readme_path = os.path.join(REPO_ROOT, "README.md")
    if not os.path.exists(readme_path):
        errors.append("README.md: file not found")
        return errors

    with open(readme_path, encoding="utf-8") as f:
        readme = f.read()

    documented = set(re.findall(r"`([^`]+\.py)`", readme.split("## Modules")[1].split("##")[0])) if "## Modules" in readme else set()
    actual = {os.path.basename(f) for f in py_files}

    for filename in sorted(actual - documented):
        errors.append(f"README.md: {filename} exists but is not listed in the Modules table")
    for filename in sorted(documented - actual):
        errors.append(f"README.md: {filename} is listed in the Modules table but does not exist")

    return errors


def main():
    py_files = sorted(glob.glob(os.path.join(REPO_ROOT, "*.py")))
    if not py_files:
        print("No .py files found in repo root")
        sys.exit(1)

    all_errors = []
    all_errors.extend(check_syntax(py_files))
    all_errors.extend(check_conventions(py_files))
    all_errors.extend(check_readme_sync(py_files))

    classified = sum(1 for f in py_files if classify(f) is not None)

    if all_errors:
        for error in all_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"\n{len(all_errors)} error(s) found ({len(py_files)} parsed, {classified} convention-checked)", file=sys.stderr)
        sys.exit(1)

    print(f"OK: {len(py_files)} parsed, {classified} convention-checked, README in sync")


if __name__ == "__main__":
    main()
