# GitHub Stars to Markdown 🚀
![Python](https://img.shields.io/badge/Python-3.11+-yellow.svg)
![uv](https://img.shields.io/badge/Built%20with-uv-purple)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

> **将你的 GitHub Stars 变成个人知识库的燃料。**
> *Turn your GitHub Stars into fuel for your personal knowledge base.*

[🇺🇸 **English README**](README_EN.md)

一个基于 `uv` 的轻量级 Python 工具，可以一键将你收藏的 GitHub 仓库 (Stars) 批量导出为 **Markdown 文件**。

它可以帮你建立**本地化的 GitHub 知识库**。导出后的文件经过**智能降噪**，去除了 Readme 中无关的徽章、广告和干扰信息，非常适合导入 **Obsidian**、**Notion** 或喂给 **AI (LLM)** 做检索增强生成 (RAG)。

---

## ✨ 核心特性

- 🛡️ **数据备份**: 将你的 Star 列表永久保存到本地，不再担心项目被删或遗忘。
- 🧹 **智能降噪**: 自动清洗 Readme 中的徽章 (Badges)、构建状态图和广告链接。**独家特性**：拥有“代码块保护机制”，清洗杂质的同时完整保留代码示例，大幅提升 AI 检索 (RAG) 的准确率。
- 📊 **元数据丰富**: 每个文件头部包含 YAML Frontmatter (Stars 数量、语言、标签、创建时间等)。
- ⚡ **Zero Setup**: 基于 `uv` 脚本模式，单文件运行，无需复杂的环境配置。

---

## 🛠️ 使用方法

### 1. 准备 Token
去 [GitHub Settings](https://github.com/settings/tokens/new) 生成一个 **Classic Token** (仅需勾选 `repo` 权限)。

### 2. 运行脚本
确保安装了 [uv](https://github.com/astral-sh/uv)，然后在终端运行：

```bash
# 自动安装依赖并运行
uv run export_stars.py
```

### 3\. 配置

脚本启动后会提示你输入：

  * **GitHub Token**: 你的访问令牌。
  * **输出目录**: 默认为当前目录 (`.`)，你也可以指定其他路径（如 `./backup` 或 Obsidian 仓库路径）。

-----

## 🤖 自动化与高级配置 (.env)

你可以创建一个 `.env` 文件（参考仓库中的 `.env.example`）来存储配置，或者直接使用环境变量，适合写入 Crontab 定时备份任务：

### 方式一：使用 .env 文件 (推荐)

1.  复制 `.env.example` 为 `.env`。
2.  填入你的 Token 和输出路径。
3.  直接运行脚本。

### 方式二：命令行参数

```bash
# Linux / Mac
GITHUB_TOKEN=your_token OUTPUT_DIR=./backup uv run export_stars.py

# Windows PowerShell
$env:GITHUB_TOKEN="your_token"; $env:OUTPUT_DIR="./backup"; uv run export_stars.py
```

-----

## 📄 导出效果示例

每个 Star 会生成一个独立的 `.md` 文件，头部包含元数据，正文经过清洗：

```markdown
---
tags: [github_star]
name: Perplexica
stars: 12000
language: TypeScript
created: 2024-05-20
---

# ItzCrazyKns/Perplexica

> 💡 **简介**: An AI-powered search engine.
> 🔗 **链接**: [https://github.com/ItzCrazyKns/Perplexica](https://github.com/ItzCrazyKns/Perplexica)

---

## 📖 项目详情

Perplexica is an AI-powered search engine...
(此处为清洗后的 Readme 正文，保留了关键代码块，去除了广告图)
```

-----

## 📜 许可证

本项目基于 **GNU General Public License v3.0 (GPLv3)** 开源。

---

## 🙏 致谢 (Acknowledgments)

- 特别感谢 **Google Gemini 3 Pro** 为本项目提供的核心代码逻辑与文档支持。