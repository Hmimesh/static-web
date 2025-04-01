from textnode import TextNode, TextType

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