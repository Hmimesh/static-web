from textnode import TextNode, TextType
from enum import Enum
from split import *
class BlockType(enum):
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
            return BlockType.heading
    if block.startswith("```") and block.endswith("```"):
        return BlockType.code
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

def main():
    node = TextNode("This is normal", TextType.NORMAL_TEXT)
    node_2 = TextNode("This is a link node", TextType.LINKS, "https://www.google.com/search?client=firefox-b-d&q=Danny+devito")
    node_3 = TextNode("This is a BOLD text", TextType.BOLD)
    node_4 = TextNode("This is an I-t-a-l-i-c text", TextType.ITALIC)
    node_5 = TextNode("This is a `code` text", TextType.CODE)
    node_6 = TextNode("this is an image text", TextType.IMAGES, "https://upload.wikimedia.org/wikipedia/commons/8/88/Danny_DeVito_cropped_and_edited_for_brightness.jpg")

    print(node)
    print(node_2)
    print(node_3)
    print(node_4)
    print(node_5)
    print(node_6)


if __name__ == "__main__":
    main()