"""Expose only the reviewed tools over local stdio; never prompt for a password."""
import json
import os
import sys

from bootstrap import ROOT, configure

directory = configure()
settings = json.loads((ROOT / "config" / "tools.json").read_text(encoding="utf-8"))
os.environ["GARMIN_ENABLED_TOOLS"] = ",".join(settings["enabled_tools"])
os.environ.pop("GARMIN_DISABLED_TOOLS", None)

import garmin_mcp

original_init = garmin_mcp.init_api


def token_only_login(email=None, password=None):
    if not (directory / "tokens" / "garmin_tokens.json").is_file():
        raise RuntimeError("尚未登录佳明中国区。请先运行 02-login.cmd，再重启 Codex。")
    return original_init(None, None)


garmin_mcp.init_api = token_only_login

if __name__ == "__main__":
    garmin_mcp.main()
