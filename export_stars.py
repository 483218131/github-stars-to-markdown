# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "PyGithub",
#     "python-dotenv",
# ]
# ///

import os
import re
import sys
from github import Github

# 尝试加载 .env 文件
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ================= 配置区 =================
# 优先从环境变量获取，方便 CI/CD 或自动化脚本调用
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OUTPUT_DIR = os.getenv("OUTPUT_DIR")
# =========================================

def sanitize_filename(name):
    """文件名消毒"""
    return re.sub(r'[\\/*?:"<>|]', '_', name).strip()

def clean_readme_noise(text):
    """强力降噪：移除徽章、图片、多余空行"""
    if not text: return "> ⚠️ 该项目没有 Readme"
    text = re.sub(r'\[?!\[.*?\]\(.*?\)]?\(.*?\)', '', text)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'<img[^>]*>', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def main():
    global GITHUB_TOKEN, OUTPUT_DIR

    print("🚀 GitHub Stars to Markdown Exporter")
    print("------------------------------------")

    # 1. 获取 Token
    if not GITHUB_TOKEN:
        GITHUB_TOKEN = input("🔑 请输入 GitHub Token (留空退出): ").strip()
        if not GITHUB_TOKEN:
            print("❌ 未提供 Token，程序退出。")
            sys.exit(1)

    # 2. 获取输出目录 (新功能)
    if not OUTPUT_DIR:
        # 默认路径：脚本运行所在的当前目录
        default_dir = os.getcwd()
        user_input = input(f"📂 请输入输出目录 (默认: 当前目录): ").strip()
        
        if user_input:
            # 支持相对路径和绝对路径
            OUTPUT_DIR = os.path.abspath(user_input)
        else:
            OUTPUT_DIR = default_dir

    if not os.path.exists(OUTPUT_DIR):
        try:
            os.makedirs(OUTPUT_DIR)
            print(f"✅ 已创建目录: {OUTPUT_DIR}")
        except Exception as e:
            print(f"❌ 无法创建目录: {e}")
            sys.exit(1)

    print(f"📝 笔记将保存至: {OUTPUT_DIR}")
    print("------------------------------------")
    print("🚀 正在连接 GitHub API...")

    try:
        g = Github(GITHUB_TOKEN)
        user = g.get_user()
        stars = user.get_starred()
        total = stars.totalCount
        print(f"📦 共检测到 {total} 个 Star，开始导出...")
    except Exception as e:
        print(f"❌ 连接失败，请检查 Token。错误: {e}")
        return

    for index, repo in enumerate(stars):
        try:
            readme_content = "> ⚠️ 无法获取 Readme"
            try:
                readme_raw = repo.get_readme().decoded_content.decode('utf-8')
                readme_content = clean_readme_noise(readme_raw)
            except:
                pass

            # 通用 Markdown 格式
            md_content = f"""---
tags: [github_star]
name: {repo.name}
author: {repo.owner.login}
url: {repo.html_url}
stars: {repo.stargazers_count}
language: {repo.language if repo.language else "Unknown"}
created: {repo.created_at.strftime("%Y-%m-%d")}
topics: [{", ".join(repo.get_topics())}]
---

# {repo.full_name}

> 💡 **简介**: {repo.description if repo.description else ""}
> 🔗 **链接**: {repo.html_url}

---

## 📖 项目详情

{readme_content}
"""
            safe_name = sanitize_filename(repo.name)
            file_path = os.path.join(OUTPUT_DIR, f"{safe_name}.md")
            
            # 简单的重名保护
            if os.path.exists(file_path):
                safe_name = sanitize_filename(f"{repo.owner.login}_{repo.name}")
                file_path = os.path.join(OUTPUT_DIR, f"{safe_name}.md")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            
            print(f"[{index+1}/{total}] ✅ 已保存: {safe_name}")

        except Exception as e:
            print(f"❌ 跳过 {repo.name}: {e}")

    print("\n🎉 导出完成！")

if __name__ == "__main__":
    main()
