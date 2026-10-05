"""Build from an explicit source allowlist, never by zipping the workspace."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parent.parent
NAME = "garmin-cn-codex-coach-0.1.0-beta.1-windows"
ROOT_FILES = {"README.md", "LICENSE", "NOTICE.md", "RELEASE_NOTES.md", "requirements.txt",
              ".gitignore", ".gitattributes", "01-install.cmd", "02-login.cmd",
              "03-connect-codex.cmd", "04-check.cmd"}
DIRECTORIES = {"app", "config", "docs", "scripts", "skills", "tests", "vendor"}
EXTENSIONS = {".py", ".json", ".md", ".ps1", ".svg"}
FORBIDDEN_COMPONENTS = {".git", ".venv", "__pycache__", "private", "tokens", "data", ".env", "dist", "build"}
FORBIDDEN_NAMES = {"athlete-profile.json", "login-status.json", "garmin_tokens.json"}


def public_files(root=ROOT):
    result = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in FORBIDDEN_COMPONENTS for part in relative.parts):
            continue
        if len(relative.parts) == 1:
            if relative.name not in ROOT_FILES:
                continue
        elif relative.parts[0] not in DIRECTORIES:
            continue
        elif path.suffix not in EXTENSIONS and relative.as_posix() != "vendor/LICENSE":
            continue
        if (relative.name in FORBIDDEN_NAMES or "token" in relative.name.lower()
                and relative.name != "token_utils.py"):
            raise RuntimeError(f"Sensitive-looking file in release source: {relative}")
        content = path.read_text(encoding="utf-8-sig")
        if re.search(r"C:[\\/]Users[\\/]", content, re.I):
            raise RuntimeError(f"Personal absolute path in {relative}")
        if re.search(r"\b(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}", content):
            raise RuntimeError(f"Credential-looking text in {relative}")
        if re.search(r"\beyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+", content):
            raise RuntimeError(f"JWT-looking text in {relative}")
        result.append(path)
    for name in ROOT_FILES:
        if not (root / name).is_file():
            raise RuntimeError(f"Missing required release file: {name}")
    return result


def build(destination: Path):
    files = public_files()
    destination.mkdir(parents=True, exist_ok=True)
    archive = destination / f"{NAME}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as output:
        for path in files:
            output.write(path, f"{NAME}/{path.relative_to(ROOT).as_posix()}")
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (destination / "SHA256SUMS.txt").write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    print(f"Release built: {len(files)} files, {archive.stat().st_size} bytes")
    print(f"SHA256: {digest}")
    return archive


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    build(args.output.resolve())
