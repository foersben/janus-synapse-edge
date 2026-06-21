import os
import re


def get_all_files(root_dir):
    all_files = set()
    for root, _dirs, files in os.walk(root_dir):
        for f in files:
            rel_path = os.path.relpath(os.path.join(root, f), root_dir)
            all_files.add(rel_path)
    return all_files


def check_links(file_path, all_files, docs_dir):
    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    # Match [text](link) and [text](<link>)
    links = re.findall(r"\[.*?\]\((<)?(.*?)(?(1)>)\)", content)

    broken = []
    for _, link in links:
        # Ignore external links
        if link.startswith("http") or link.startswith("#") or link.startswith("mailto:"):
            continue

        # Clean up link (remove anchors)
        clean_link = link.split("#")[0]
        if not clean_link:
            continue

        # Resolve relative link
        file_dir = os.path.dirname(file_path)
        abs_link = os.path.normpath(os.path.join(file_dir, clean_link))
        rel_to_root = os.path.relpath(abs_link, os.getcwd())

        if not os.path.exists(rel_to_root):
            broken.append((link, rel_to_root))

    return broken


docs_dir = "docs"
all_files = get_all_files(".")
md_files = [os.path.join(docs_dir, f) for f in os.listdir(docs_dir) if f.endswith(".md")]
md_files.append("README.md")

for md in md_files:
    broken = check_links(md, all_files, docs_dir)
    if broken:
        print(f"File: {md}")
        for link, path in broken:
            print(f"  Broken Link: {link} -> {path}")
