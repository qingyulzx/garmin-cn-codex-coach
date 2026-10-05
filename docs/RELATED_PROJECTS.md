# GitHub 同类项目调研

调研日期：2026-10-05。以下对比依据项目公开 README；除本项目所用的 Taxuspt 固定版本外，没有安装并完整验证其他项目，不能据此排名性能或稳定性。

| 项目 | 已公开的方向 | 与本项目的关系 |
|---|---|---|
| [Taxuspt/garmin_mcp](https://github.com/Taxuspt/garmin_mcp) | 通用 Garmin MCP，提供中国区环境开关、多类数据工具 | 本项目的直接上游，工具源码与 MIT 许可保留 |
| [BorisBW/garmin-mcp-cn](https://github.com/BorisBW/garmin-mcp-cn) | 明确面向 garmin.cn 的 Garmin MCP 分支 | 说明中国区 MCP 已有先例，不应宣称本项目首创 |
| [BorisBW/claude-fitness-cn](https://github.com/BorisBW/claude-fitness-cn) | 面向 Claude Code 的 AI 健身教练，提供多设备与记忆工作流 | 说明“数据连接 + 教练指令 + 记忆”的组合已有先例；本项目未复制其技能或评分公式 |
| [KaiChen-Zhong/garmin-cn-coach-stack](https://github.com/KaiChen-Zhong/garmin-cn-coach-stack) | 中国区数据、MCP、报告与本地自动化工具链 | 功能范围比本测试版广；未验证其安装流程 |
| [stitrace/garmin-mcp-server](https://github.com/stitrace/garmin-mcp-server) | 另一个支持中国区配置的本地 Garmin MCP | 同类数据接入方案；未验证其工具覆盖 |

本项目定位：**基于已存在的 Garmin MCP 能力，提供面向 Windows / Codex 新用户的中文登录、固定依赖、只读工具配置和跑步专项分析流程。**

这些项目的存在不代表获得 Garmin 官方接口授权，也不代表已进入 OpenAI 官方插件目录。
