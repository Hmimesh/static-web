from textnode import TextNode, TextType
from enum import Enum
from split import *
from markdown_to_blocks import *
import os
import shutil

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
    public = "./public/"
    if os.path.exists(public):
        shutil.rmtree("./public/")
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
    copy_recursive(static, public)
    


def main():
   content_to_destination()


if __name__ == "__main__":
    main()