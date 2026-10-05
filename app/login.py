"""Authenticate locally without writing or echoing the supplied password."""
from __future__ import annotations

import argparse
import csv
import io
import os
import subprocess
import sys

from bootstrap import configure


def restrict_directory(path):
    path.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        identity = subprocess.run(["whoami", "/user", "/fo", "csv", "/nh"],
                                  check=True, capture_output=True, text=True)
        sid = next(csv.reader(io.StringIO(identity.stdout.strip())))[1]
        subprocess.run(["icacls", str(path), "/inheritance:r", "/grant:r",
                        f"*{sid}:(OI)(CI)F", "*S-1-5-18:(OI)(CI)F"],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        path.chmod(0o700)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force-reauth", action="store_true")
    options = parser.parse_args()
    directory = configure()
    restrict_directory(directory)
    token_path = directory / "tokens"
    restrict_directory(token_path)
    from garminconnect import Garmin
    from login_dialog import ask_credentials, ask_mfa

    if not options.force_reauth and (token_path / "garmin_tokens.json").is_file():
        try:
            client = Garmin(is_cn=True)
            client.login(str(token_path))
            if client.get_full_name():
                print("现有登录有效，可以运行 03-connect-codex.cmd。")
                return 0
        except Exception:
            print("现有登录已失效或暂时无法验证，将重新登录。")

    print("请在本机窗口填写 Garmin 中国区账号。密码默认隐藏，可点“显示密码”。")
    print("密码和验证码只用于本次登录；程序保存的是登录令牌，不保存密码。")
    try:
        email, password = ask_credentials()
        client = Garmin(email=email, password=password, is_cn=True,
                        prompt_mfa=ask_mfa, return_on_mfa=True)
        result, context = client.login()
        if result == "needs_mfa":
            client.resume_login(context, ask_mfa())
        client.client.dump(str(token_path))
        if os.name != "nt":
            for item in token_path.iterdir():
                if item.is_file():
                    item.chmod(0o600)
        check = Garmin(is_cn=True)
        check.login(str(token_path))
        if not check.get_full_name():
            raise RuntimeError("saved_session_not_authenticated")
    except (KeyboardInterrupt, EOFError):
        print("登录已取消。")
        return 1
    except Exception as error:
        # Do not print raw HTTP responses, account names, or authentication secrets.
        print(f"登录未成功（{type(error).__name__}）。")
        print("连接中断、SSL、JWT 或限流错误不一定表示密码错误。稍候重试并查看 docs/TROUBLESHOOTING.md。")
        print("反馈问题时不要提供密码、验证码或 tokens 文件。")
        return 1
    print("登录验证成功。请运行 03-connect-codex.cmd，随后完全退出并重新打开 Codex。")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
