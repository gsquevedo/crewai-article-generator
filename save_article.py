import os
import json
from datetime import datetime
import re

def _sanitize_filename(text):
    return re.sub(r'\W+', '_', text.lower())[:50]

def save_article_as_md(title: str, content: str, directory: str = "artigos_salvos"):
    os.makedirs(directory, exist_ok=True)
    filename = f"{_sanitize_filename(title)}.md"
    path = os.path.join(directory, filename)

    with open(path, 'w', encoding='utf-8') as file:
        file.write(f"# {title}\n\n{content}")

    print(f"✅ Artigo salvo como Markdown: {path}")
    return path

def save_article_as_json(title: str, content: str, directory: str = "artigos_salvos"):
    os.makedirs(directory, exist_ok=True)
    filename = f"{_sanitize_filename(title)}.json"
    path = os.path.join(directory, filename)

    data = {
        "title": title,
        "content": content,
        "timestamp": datetime.now().isoformat()
    }

    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"✅ Artigo salvo como JSON: {path}")
    return path
