"""Shared paths and environment for the local China-region connector."""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERVER_NAME = "garmin_cn_coach"
VERSION = "0.1.0-beta.1"


def data_dir() -> Path:
    override = os.environ.get("GARMIN_CN_COACH_DATA_DIR")
    if override:
        return Path(override).expanduser().resolve()
    if os.name == "nt":
        return Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / "GarminCnCodexCoach"
    return Path.home() / ".local" / "share" / "garmin-cn-codex-coach"


def configure() -> Path:
    directory = data_dir()
    os.environ["GARMIN_IS_CN"] = "true"
    os.environ["GARMINTOKENS"] = str(directory / "tokens")
    os.environ["GARMINTOKENS_BASE64"] = str(directory / "unused-base64")
    os.environ["GARMIN_MCP_TRANSPORT"] = "stdio"
    os.environ["GARMIN_MCP_CALL_TIMEOUT"] = "60"
    for key in ("GARMIN_EMAIL", "GARMIN_PASSWORD", "GARMIN_EMAIL_FILE", "GARMIN_PASSWORD_FILE"):
        os.environ.pop(key, None)
    sys.path.insert(0, str(ROOT / "vendor"))
    return directory
