from textnode import TextNode, TextType
from enum import Enum
from split import *
from markdown_to_blocks import *
import os
import shutil
import sys

if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "/"
if not basepath.endswith("/"):
    basepath = basepath + "/"
if not basepath.startswith("/"):
    basepath = "/" +basepath

class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6

def block_to_block_type(block):
    lines = block.split("\n")
    for i in range(1, 7):
        prefix = "#" * i + " "
        if block.startswith(prefix):
            return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def content_to_destination():
    static = "./static/"
    docs = "./docs/"
    if os.path.exists(docs):
        shutil.rmtree("./docs/")
    def copy_recursive(src, dst):
        if os.path.isdir(src):
            print(f'copying {src} to {dst}')
            if not os.path.exists(dst):
                os.mkdir(dst)
            for file in os.listdir(src):
                copy_recursive(os.path.join(src, file), os.path.join(dst, file))
        else:
            print(f'copying {src} to {dst}')
            shutil.copy(src, dst)
    copy_recursive(static, docs)
    
def extrac_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith('#'):
            return line[1:] .strip()
    raise ValueError("No title found")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f'Generating {from_path} to {dest_path} using {template_path}')
    with open(from_path, "r") as f:
        markdown  = f.read()
    with open(template_path, 'r') as f:
        template = f.read()
    node = markdown_to_html_node(markdown)
    better_n = node.to_html()
    title = extrac_title(markdown)
    final = template.replace("{{ Content }}", better_n).replace("{{ Title }}", title)
    final = final.replace('href="/', f'href="{basepath}')
    final = final.replace('src="/', f'src="{basepath}')
    with open(dest_path, "w") as f:
        f.write(final)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    content = os.listdir(dir_path_content)
    for file in content:
        if file.endswith(".md"):
            from_path = os.path.join(dir_path_content, file)
            dest_path = os.path.join(dest_dir_path, file.replace(".md", ".html"))
            generate_page(from_path, template_path, dest_path, basepath)
        elif os.path.isdir(os.path.join(dir_path_content, file)):
            if not os.path.isdir(os.path.join(dest_dir_path, file)):
                os.makedirs(os.path.join(dest_dir_path, file))
            generate_pages_recursive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file), basepath)
    


def main():

   content_to_destination()
   generate_pages_recursive("./content", "./template.html", "./docs", basepath)


if __name__ == "__main__":
    main()