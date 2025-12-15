# GitHub Stars to Markdown 🚀

![Python](https://img.shields.io/badge/Python-3.11+-yellow.svg)
![uv](https://img.shields.io/badge/Built%20with-uv-purple)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

> **Turn your GitHub Stars into fuel for your personal knowledge base.**

[🇨🇳 **中文说明 (Chinese README)**](README.md)

A lightweight Python tool based on `uv` that batches exports your GitHub starred repositories into clean, local **Markdown files**.

It helps you build a **localized GitHub knowledge base**. The exported files are **intelligently cleaned**, removing irrelevant badges, ads, and noise from the Readme. This makes them perfect for **Obsidian**, **Notion**, or as high-quality context for **AI (LLM)** Retrieval-Augmented Generation (RAG).

---

## ✨ Features

- 🛡️ **Data Backup**: Save your Star list locally forever. Never worry about deleted repositories again.
- 🧹 **Smart Noise Reduction**: Automatically cleans badges, build status icons, and ad links. **Exclusive Feature**: Includes a "Code Block Protection" mechanism that cleans noise while strictly preserving code examples, drastically improving AI indexing (RAG) accuracy.
- 📊 **Rich Metadata**: Each file includes YAML Frontmatter (Stars count, Language, Topics, Created Date, Author, etc.).
- ⚡ **Zero Setup**: Runs in `uv` script mode. Single-file execution, no complex environment configuration required.

---

## 🛠️ Usage

### 1. Prepare Token
Go to [GitHub Settings](https://github.com/settings/tokens/new) and generate a **Classic Token** (select `repo` scope only).

### 2. Run Script
Ensure [uv](https://github.com/astral-sh/uv) is installed, then run in your terminal:

```bash
# Automatically installs dependencies and runs
uv run export_stars.py
```

### 3\. Configuration

The script will prompt you for:

  * **GitHub Token**: Your personal access token.
  * **Output Directory**: Defaults to the current directory (`.`), or specify a custom path (e.g., `./backup` or your Obsidian vault path).

-----

## 🤖 Automation & Advanced Config (.env)

You can create a `.env` file (see `.env.example` in the repo) or use environment variables to skip interactive prompts, ideal for Crontab backup tasks:

### Method 1: Use .env file (Recommended)

1.  Copy `.env.example` to `.env`.
2.  Fill in your Token and Output Directory.
3.  Run the script.

### Method 2: Command Line Arguments

```bash
# Linux / Mac
GITHUB_TOKEN=your_token OUTPUT_DIR=./backup uv run export_stars.py

# Windows PowerShell
$env:GITHUB_TOKEN="your_token"; $env:OUTPUT_DIR="./backup"; uv run export_stars.py
```

-----

## 📄 Output Example

Each Star generates an independent `.md` file with metadata and cleaned content:

```markdown
---
tags: [github_star]
name: Perplexica
stars: 12000
language: TypeScript
created: 2024-05-20
---

# ItzCrazyKns/Perplexica

> 💡 **Description**: An AI-powered search engine.
> 🔗 **Link**: [https://github.com/ItzCrazyKns/Perplexica](https://github.com/ItzCrazyKns/Perplexica)

---

## 📖 Project Details

Perplexica is an AI-powered search engine...
(Cleaned Readme content here, code blocks preserved, ads removed)
```

-----

## 📜 License

This project is open-sourced under the **GNU General Public License v3.0 (GPLv3)**.

-----

## 🙏 Acknowledgments

  * Special thanks to **Google Gemini 3 Pro** for assisting with the core logic and documentation.