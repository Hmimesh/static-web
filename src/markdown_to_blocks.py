import re
from split import markdown_to_blocks, text_to_textnode
from htmlnode import ParentNode, LeafNode, text_node_to_html_node
from main import BlockType, block_to_block_type




def text_to_children(text):
    return [text_node_to_html_node(n) for n in text_to_textnode(text)]


def heading_to_html(block):
    # Count leading '#'
    i = 0
    while i < len(block) and i < 6 and block[i] == '#':
        i += 1
    text = block[i:].lstrip()
    level = max(1, min(i, 6))
    return ParentNode(f"h{level}", text_to_children(text.strip()))


def paragraph_to_html(block):
    text = " ".join(line.strip() for line in block.splitlines()).strip()
    return ParentNode("p", text_to_children(text))


def quote_to_html(block):
    lines = []
    for line in block.splitlines():
        if line.startswith(">"):
            line = line[1:].lstrip()
        lines.append(line)
    text = " ".join(lines).strip()
    return ParentNode("blockquote", text_to_children(text))


def ul_to_html(block):
    items = []
    for line in block.splitlines():
        items.append(ParentNode("li", text_to_children(line[2:].strip())))
    return ParentNode("ul", items)


def ol_to_html(block):
    items = []
    for line in block.splitlines():
        text = re.sub(r"^\d+\.\s+", "", line).strip()
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", items)


def code_to_html(block):
    lines = block.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    code_text = "\n".join(lines)
    return ParentNode("pre", [LeafNode("code", code_text)])


def markdown_to_html_node(markdown):
    children = []
    for block in markdown_to_blocks(markdown):
        bt = block_to_block_type(block)
        if bt == BlockType.HEADING:
            children.append(heading_to_html(block))
        elif bt == BlockType.CODE:
            children.append(code_to_html(block))
        elif bt == BlockType.QUOTE:
            children.append(quote_to_html(block))
        elif bt == BlockType.UNORDERED_LIST:
            children.append(ul_to_html(block))
        elif bt == BlockType.ORDERED_LIST:
            children.append(ol_to_html(block))
        else:
            children.append(paragraph_to_html(block))
    return ParentNode("div", children)