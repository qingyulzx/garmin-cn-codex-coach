"""Append one MCP entry; preserve existing config and refuse name collisions."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import tomllib

from bootstrap import ROOT, SERVER_NAME


def server_entry(python: Path) -> str:
    return (f"\n[mcp_servers.{SERVER_NAME}]\n"
            f"command = {json.dumps(str(python), ensure_ascii=False)}\n"
            f"args = [{json.dumps(str(ROOT / 'app' / 'run_server.py'), ensure_ascii=False)}]\n"
            "enabled = true\nstartup_timeout_sec = 30\ntool_timeout_sec = 75\n")


def register(config: Path, python: Path, dry_run=False):
    original = config.read_text(encoding="utf-8-sig") if config.exists() else ""
    parsed = tomllib.loads(original)
    existing = parsed.get("mcp_servers", {}).get(SERVER_NAME)
    if existing is not None:
        if (existing.get("command") == str(python) and
                existing.get("args") == [str(ROOT / "app" / "run_server.py")]):
            return "already-configured"
        raise RuntimeError("已有同名 MCP 指向其他目录。未改动原配置；请先在 Codex 设置中移除旧的 garmin_cn_coach 项。")
    new = original + server_entry(python)
    tomllib.loads(new)
    if not dry_run:
        config.parent.mkdir(parents=True, exist_ok=True)
        # Recheck before append, so a concurrent editor isn't overwritten.
        current = config.read_text(encoding="utf-8-sig") if config.exists() else ""
        if current != original:
            raise RuntimeError("配置刚被其他程序修改，请重试。")
        with config.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(server_entry(python))
    return "dry-run-ok" if dry_run else "added"


def install_skill(home: Path, dry_run=False):
    source = ROOT / "skills" / "garmin-cn-running-coach"
    target = home / "skills" / source.name
    if target.exists():
        source_files = {p.relative_to(source) for p in source.rglob("*") if p.is_file()}
        target_files = {p.relative_to(target) for p in target.rglob("*") if p.is_file()}
        if source_files != target_files or any((source / p).read_bytes() != (target / p).read_bytes() for p in source_files):
            raise RuntimeError("已有不同版本的同名教练 Skill，未覆盖；请保留旧版或手动更新。")
        return "already-installed"
    if not dry_run:
        shutil.copytree(source, target)
    return "dry-run-ok" if dry_run else "installed"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--codex-home", type=Path)
    parser.add_argument("--python", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    options = parser.parse_args()
    home = options.codex_home or Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    python = (options.python or Path(sys.executable)).resolve()
    # Preflight both changes before applying either.
    register(home / "config.toml", python, dry_run=True)
    install_skill(home, dry_run=True)
    print("MCP:", register(home / "config.toml", python, options.dry_run))
    print("教练 Skill:", install_skill(home, options.dry_run))
    if not options.dry_run:
        print("请完全退出并重新打开 Codex，再问：请分析我最近四周的跑步训练。")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        main()
    except Exception as error:
        print(f"配置未完成：{error}", file=sys.stderr)
        raise SystemExit(1)
