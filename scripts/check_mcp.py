"""Offline protocol/allowlist check using an empty, isolated token directory."""
import json
from pathlib import Path
import sys
import tempfile
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))

import anyio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def check():
    from garminconnect import Garmin
    client = Garmin(is_cn=True).client
    endpoints = (client._sso, client._connect, client._connectapi,
                 client._ios_service_url, client._mobile_sso_service_url,
                 client._portal_service_url, client._di_token_url)
    if not all((urlparse(url).hostname or "").endswith(".garmin.cn") for url in endpoints):
        raise RuntimeError("China-region endpoint verification failed.")
    expected = set(json.loads((ROOT / "config" / "tools.json").read_text(encoding="utf-8"))["enabled_tools"])
    with tempfile.TemporaryDirectory(prefix="garmin-cn-mcp-check-") as directory:
        server = StdioServerParameters(command=sys.executable,
                                       args=["-B", str(ROOT / "app" / "run_server.py")],
                                       env={"GARMIN_CN_COACH_DATA_DIR": directory})
        with anyio.fail_after(30):
            async with stdio_client(server) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.list_tools()
                    names = {tool.name for tool in result.tools}
                    if names != expected:
                        raise RuntimeError(f"Tool allowlist mismatch: missing={sorted(expected-names)}, extra={sorted(names-expected)}")
                    # With no credentials, a data call must fail rather than log in elsewhere.
                    failure = await session.call_tool("get_activities", {"start": 0, "limit": 1})
                    error_text = "\n".join(block.text for block in failure.content if block.type == "text")
                    # Upstream catches API exceptions and returns text; isError can be false.
                    if "尚未登录佳明中国区" not in error_text or "02-login.cmd" not in error_text:
                        raise RuntimeError("No-token data call did not return the expected login guard.")
    print(json.dumps({"china_endpoints": "passed", "mcp_initialization": "passed",
                      "tool_count": len(names), "no_token_guard": "passed",
                      "personal_data_queried": False}))


if __name__ == "__main__":
    anyio.run(check)
