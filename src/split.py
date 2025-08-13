from textnode import TextNode, TextType
import re
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_node.append(old_node)
            continue
        split_nodes = []
        section = old_node.text.split(delimiter)
        if len(section) % 2 == 0:
            raise ValueError("invvalid markdown, formatted section not closee")
        for i in range(len(section)):
            if section[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(section[i], TextType.NORMAL_TEXT))
            else:
                split_nodes.append(TextNode(section[i], text_type))
        new_node.extend(split_nodes)
    return new_node

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        remaining_text = old_node.text
        images = extract_markdown_images(remaining_text)

        for alt_text, url in images:
            pre_image, remaining_text = remaining_text.split(f'![{alt_text}]({url})', 1)
            if pre_image:
                split_nodes.append(TextNode(pre_image, TextType.NORMAL_TEXT))
                split_nodes.append(TextNode(alt_text, TextType.IMAGES, url))
        if remaining_text:
            split_nodes.append(TextNode(remaining_text, TextType.NORMAL_TEXT))
        
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        remaining_text = old_node.text
        links = extract_markdown_links(remaining_text)

        for alt_text, url in links:
            pre_link, remaining_text = remaining_text.split(f'[{alt_text}]({url})', 1)
            if pre_link:
                split_nodes.append(TextNode(pre_link, TextType.NORMAL_TEXT))
                split_nodes.append(TextNode(alt_text, TextType.LINKS, url))
        if remaining_text:
            split_nodes.append(TextNode(remaining_text, TextType.NORMAL_TEXT))

        new_nodes.extend(split_nodes)
    return new_nodes



def text_to_textnode(text):
    nodes = [TextNode(text, TextType.NORMAL_TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = []
    block = markdown.split("\n\n")
    for b in block:
        stripped_block = b.strip("")
        if stripped_block:
            blocks.append(stripped_block)
    return blocks

