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
import html
from github import Github, Auth

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ================= 配置区 =================
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OUTPUT_DIR = os.getenv("OUTPUT_DIR")
# =========================================

def sanitize_filename(name):
    # 统一将文件名非法字符换成下划线
    return re.sub(r'[\\/*?:"<>|]', '_', name).strip()

def clean_readme_noise(text):
    """
    强力降噪 v9.0 (修复误杀文字、实体符、相对链接、残留标签)
    """
    if not text: return "> ⚠️ 该项目没有 Readme"

    # --- 步骤 0: HTML 实体解码 (解决 &ensp; &nbsp; 问题) ---
    # 把 &quot; &gt; 等转回正常字符
    text = html.unescape(text)

    # --- 步骤 1: 保护代码块 ---
    code_blocks = []
    def save_code_block(match):
        code_blocks.append(match.group(0))
        return f"__CODE_BLOCK_{len(code_blocks)-1}__"
    
    text = re.sub(r'```[\s\S]*?```', save_code_block, text)

    # --- 步骤 2: 暴力清洗 HTML ---
    
    # 移除 HTML 注释
    text = re.sub(r'', '', text, flags=re.DOTALL)
    # 移除 <style>, <script>, <details> (包含内容)
    text = re.sub(r'<(style|script|details).*?>.*?</\1>', '', text, flags=re.DOTALL)
    
    # 【关键】移除 HTML 标签，但保留内容 (除了 div/p/a 这种容器)
    # 先把 <div...> ... </div> 这种不仅删标签，里面的图片链接往往也是噪音，但文字要保留
    # 这里我们简化策略：直接删掉所有 <...> 格式的标签字符串
    text = re.sub(r'<[^>]+>', ' ', text)

    # --- 步骤 3: 链接与图片清洗 (精细化操作) ---

    # 1. 移除 Markdown 图片 ![alt](url) -> 删掉
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    
    # 2. 移除带链接的图片壳子 [![alt](img)](link) -> 删掉
    text = re.sub(r'\[!\[.*?\]\(.*?\)]\(.*?\)', '', text)

    # 3. 【关键修复】处理普通链接 [Text](Url)
    # 如果 Url 是相对路径 (./xxx 或 ../xxx)，直接删掉整个链接 (因为本地跳不过去)
    text = re.sub(r'\[.*?\]\((\./|\.\./).*?\)', '', text)
    
    # 4. 【关键修复】保留文字，只去链接： [Text](http...) -> Text
    # 之前是直接删掉，导致 "☑ [Feature]" 变成了 "☑ "
    def link_to_text(match):
        text_content = match.group(1)
        url_content = match.group(2)
        # 如果是锚点链接 (#xxx) 或者空链接，直接删
        if url_content.startswith('#') or not text_content.strip():
            return ""
        return text_content # 只保留文字

    text = re.sub(r'\[(.*?)\]\((.*?)\)', link_to_text, text)

    # --- 步骤 4: 逐行精修 ---
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        s_line = line.strip()
        
        # 1. 跳过空行和纯占位符行
        if not s_line: 
            cleaned_lines.append("") # 保持段落感
            continue

        # 2. 跳过幽灵列表 (- - -)
        if re.match(r'^[-*]\s*$', s_line): continue
        
        # 3. 跳过表格分隔线 (但保留表格头)
        # if re.match(r'^\|?[-:| ]+\|?$', s_line): continue 
        # (V8版有人反馈表格没了，这里保守一点，先不删分隔线，交给Obsidian渲染)

        # 4. 跳过纯标点符号行 (解决你截图里那个单独的 <a ...></a> 留下的空壳)
        if re.match(r'^[|·\s<>]+$', s_line): continue

        cleaned_lines.append(line.rstrip())
    
    text = '\n'.join(cleaned_lines)

    # --- 步骤 5: 归还代码块 ---
    def restore_code_block(match):
        index = int(match.group(1))
        return code_blocks[index]
    
    text = re.sub(r'__CODE_BLOCK_(\d+)__', restore_code_block, text)

    # --- 步骤 6: 最终整形 ---
    # 移除空的代码块壳子 (``` \n ```)
    text = re.sub(r'```[a-z]*\s*\n\s*```', '', text, flags=re.DOTALL)
    
    # 压缩多余空行
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

def main():
    global GITHUB_TOKEN, OUTPUT_DIR
    print("🚀 GitHub Stars to Markdown (V9.0 Final Fix)")
    
    if not GITHUB_TOKEN:
        GITHUB_TOKEN = input("🔑 请输入 GitHub Token: ").strip()
        if not GITHUB_TOKEN:
            print("❌ 未提供 Token，退出。")
            sys.exit(1)

    if not OUTPUT_DIR:
        default_dir = os.getcwd()
        user_input = input(f"📂 输出目录 (默认: 当前目录): ").strip()
        OUTPUT_DIR = os.path.abspath(user_input) if user_input else default_dir

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print("🚀 正在连接 GitHub API...")

    try:
        auth = Auth.Token(GITHUB_TOKEN)
        g = Github(auth=auth)
        stars = g.get_user().get_starred()
        total = stars.totalCount
        print(f"📦 检测到 {total} 个 Star，开始处理...")
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return

    for index, repo in enumerate(stars):
        try:
            readme_content = "> ⚠️ 无法获取 Readme"
            try:
                readme_raw = repo.get_readme().decoded_content.decode('utf-8')
                readme_content = clean_readme_noise(readme_raw)
            except:
                pass

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
            # 文件名处理逻辑优化：直接用 "项目名.md"
            # 只有当重名时，才加 "作者_项目名.md"
            safe_name = sanitize_filename(repo.name)
            file_path = os.path.join(OUTPUT_DIR, f"{safe_name}.md")
            
            if os.path.exists(file_path):
                # 如果文件已存在（重名），则加上作者名区分
                safe_name = sanitize_filename(f"{repo.owner.login}_{repo.name}")
                file_path = os.path.join(OUTPUT_DIR, f"{safe_name}.md")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            
            print(f"[{index+1}/{total}] ✅ 已保存: {safe_name}")

        except Exception as e:
            print(f"❌ 跳过: {e}")

    print("\n🎉 导出完成！")

if __name__ == "__main__":
    main()
