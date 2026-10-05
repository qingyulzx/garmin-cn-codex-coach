# Garmin CN Codex Coach

支持 Garmin Connect **中国区（garmin.cn）**的 Windows / Codex 跑步分析社区测试套件。

它把本地 MCP 数据连接、中文登录窗口和跑步教练 Skill 放在一起，帮助你用自然语言分析跑量、分圈、近期训练与比赛准备。**不是 Garmin 或 OpenAI 官方产品，也不是第一个支持中国区的 Garmin MCP。**

版本：`0.1.0-beta.1`。目前仅按 Windows 11 + Python 3.12 + Codex 桌面应用的流程进行验证。需要联网安装依赖，发布包不包含 Python 或第三方运行时。

## 这个项目做了什么

- 基于 [Taxuspt/garmin_mcp](https://github.com/Taxuspt/garmin_mcp)，固定已验证源码版本，保留上游 MIT 许可和署名。
- 默认连接中国区；使用 `garminconnect 0.3.17`，处理旧版本中国区认证端点的问题。
- 提供本机中文登录窗口：密码默认隐藏、可切换显示，不写入配置文件。
- 提供 **34 个经过筛选的只读 MCP 工具**，读取活动、分圈、睡眠摘要及可用的训练指标；不注册活动修改、删除或课表写入工具。
- 用脚本追加独立的 `garmin_cn_coach` 配置项，并安装通用的跑步分析 Skill。
- 密码只用于本机登录；令牌存于个人应用数据目录，和项目源码分开。

这不是自主运行的私人教练服务：AI 分析由你使用的 Codex 模型完成。本测试版不会在后台定时同步，也不提供测量出来的乳酸阈、医学诊断或经过验证的比赛成绩预测。

## Windows 安装：按顺序双击三个文件

1. 从 GitHub **Releases** 下载 `garmin-cn-codex-coach-0.1.0-beta.1-windows.zip`，解压到一个准备长期保留的目录。不要在 ZIP 预览窗口内直接运行。
2. 安装 [Python 3.12 或更新版本](https://www.python.org/downloads/windows/)，保留 **Tcl/Tk and IDLE** 组件。首次安装时勾选 **Add python.exe to PATH** 会更方便。
3. 双击 **`01-install.cmd`**：创建独立 `.venv`，从 PyPI 安装依赖。无需 Git、Node.js 或管理员权限。网络失败可重试。
4. 双击 **`02-login.cmd`**：在弹出的本机窗口填写中国区账号和密码；若需要验证码，另一个窗口会提示。不要把密码、验证码或令牌发给 AI。
5. 双击 **`03-connect-codex.cmd`**：追加 MCP 配置和教练 Skill。它保留原有配置；遇到同名但不同路径的安装时，会停止而不是覆盖。
6. **完全退出并重新打开 Codex**。询问“请使用 Garmin 数据分析我最近四周的跑步训练”。

可选：运行 **`04-check.cmd`** 检查中国区端点、MCP 初始化和 34 个工具名单。它不查询个人训练数据，也不证明你已经登录成功；实际读数据时才会验证已保存的会话。

如果要迁移安装目录，请先在 Codex 设置中移除旧的 `garmin_cn_coach` 项，再重新运行安装和配置脚本。Python 虚拟环境和 MCP 配置依赖安装路径。已有 `garmin_cn` 等其他服务器不会被改动；避免同时让两个 Garmin 服务器执行重复的数据查询。

## 可以这样问

- “分析最近八周和最近两周的跑量、训练连续性与强度分布，按距离拆分快段和热身恢复段。”
- “这是周二课表，结合最近实际训练给我建议。我的比赛目标是……。”
- “这次操场活动是标准 5 公里，GPS 多算了距离，请按实际距离分析。”
- “我的高度数据不可靠，后续忽略爬升。”

首次使用请补充目标、日常课表、身体状态和设备数据限制。项目没有预置任何真实使用者的目标或训练历史。个性设置可参考 `config/athlete-profile.example.json`，个人档案放在应用数据目录，**不要提交到仓库**。

## 数据在哪里、会发给谁

- Garmin 登录请求由本机程序发往 Garmin；这是基于社区库的非官方接入，会受到 Garmin 接口变化、限流和登录要求影响。
- Windows 令牌目录：`%LOCALAPPDATA%\GarminCnCodexCoach\tokens`。登录脚本会限制该应用数据目录的访问权限。令牌等同登录凭据，不要分享。
- 项目不运营中转服务器，不保存云端账号数据库，也不加入统计或广告服务。
- **调用 MCP 工具返回的训练和健康数据会进入 Codex 会话，用于 AI 分析。** 本地运行不等于分析数据完全不离开电脑；请同时了解你所使用的 Codex / OpenAI 数据设置。
- 安装依赖时会访问 PyPI；访问 GitHub、Garmin、Codex 也分别受其服务条款和数据政策约束。

详见 [隐私说明](docs/PRIVACY.md)、[故障排查](docs/TROUBLESHOOTING.md) 和 [同类项目调研](docs/RELATED_PROJECTS.md)。

## 移除

在 Codex 设置中移除 `garmin_cn_coach` MCP。教练 Skill 位于 `%USERPROFILE%\.codex\skills\garmin-cn-running-coach`（设置了 `CODEX_HOME` 时在该目录下）。如果不再需要登录，可手动删除上述应用数据目录；令牌不会随着源码目录一起删除。

## 开发与检查

```powershell
.venv\Scripts\python.exe -B -m unittest discover -s tests -v
.venv\Scripts\python.exe -B scripts\check_mcp.py
.venv\Scripts\python.exe -B scripts\build_release.py
```

发布脚本只从明确允许的源码目录打包，不包含 `.venv`、`.git`、令牌、训练记录或日志，并生成 SHA-256 校验文件。构建报告与已验证范围见 [测试说明](docs/VALIDATION.md)。

## 来源与许可

Garmin MCP 数据工具来自 **Alexandre Domingues / Taxuspt**，固定提交：`cfc5d799ab0f165e837f1188a1d093c65838aaf7`。`vendor/garmin_mcp` 是该提交的未改动 Python 源码；包装脚本通过运行时配置限制工具和登录方式。

底层认证和 Garmin 接口依赖 [cyberjunky/python-garminconnect](https://github.com/cyberjunky/python-garminconnect)。中国区功能并非本项目原创；本项目主要增加 Windows 安装与登录引导、Codex 配置、只读工具选择和跑步分析流程。

本项目采用 MIT 许可，见 `LICENSE`、`NOTICE.md` 和 `vendor/LICENSE`。开源代码许可不代表获得 Garmin 官方 API 授权，也不代表符合官方插件市场审核条件。
