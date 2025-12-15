# GitHub Stars to Markdown 🚀
Gemini 3 Pro Thinking写的

一个轻量级的 Python 工具，用于将你收藏的 GitHub 仓库 (Stars) 批量导出为 **Markdown 文件**。

它可以帮你建立**本地化的 GitHub 知识库**。导出后的文件干净、纯粹，兼容任何 Markdown 编辑器（如 VS Code, Obsidian, Typora, Logseq 等）。

## ✨ 核心特性

- **数据备份**: 将你的 Star 列表永久保存到本地，不再担心项目被删或遗忘。
- **智能降噪**: 自动清洗 Readme 中的徽章 (Badges)、构建状态图和广告链接，只保留核心文本，**非常适合喂给 AI (LLM) 做知识库索引 (RAG)**。
- **元数据丰富**: 每个文件都包含 YAML Frontmatter (Stars 数量、语言、标签、创建时间等)。
- **Zero Setup**: 基于 `uv` 脚本模式，单文件运行，无需复杂的环境配置。

## 🛠️ 使用方法

### 1. 准备 Token
去 [GitHub Settings](https://github.com/settings/tokens/new) 生成一个 Classic Token (仅需勾选 `repo` 权限)。

### 2. 运行脚本
确保安装了 [uv](https://github.com/astral-sh/uv)，然后在终端运行：

```bash
uv run export_stars.py
```

### 3\. 配置

脚本启动后会提示你输入：

1.  **GitHub Token**: 你的访问令牌。
2.  **输出目录**: 默认为当前目录 (`.`)，你也可以指定其他路径（如 `./backup` 或 `/Users/name/Obsidian/Stars`）。

## 🤖 自动化 / 高级用法

你可以通过环境变量来跳过交互式输入，适合写入 Crontab 定时备份任务：

```bash
# Linux / Mac
GITHUB_TOKEN=your_token OUTPUT_DIR=./backup uv run export_stars.py

# Windows PowerShell
$env:GITHUB_TOKEN="your_token"; $env:OUTPUT_DIR="./backup"; uv run export_stars.py
```

## 📄 导出效果示例

每个 Star 会生成一个独立的 `.md` 文件：

```markdown
---
tags: [github_star]
name: Perplexica
stars: 12000
language: TypeScript
---

# ItzCrazyKns/Perplexica

> 💡 **简介**: An AI-powered search engine.
> 🔗 **链接**: [https://github.com/ItzCrazyKns/Perplexica](https://github.com/ItzCrazyKns/Perplexica)

---

## 📖 项目详情

Perplexica is an AI-powered search engine...
(此处为清洗后的 Readme 正文)
```
