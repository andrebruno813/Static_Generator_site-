from textnode import TextNode, TextType
from htmlnode import HTMLNode
from blocktype import BlockType, block_to_block_type
from markdown_blocks import markdown_to_blocks
from text_to_textnodes import text_to_textnodes
from textnode import text_node_to_html_node


def text_to_children(text):
    text_nodes = text_to_textnodes(text)

    children = []

    for text_node in text_nodes:
        children.append(
            text_node_to_html_node(text_node)
        )

    return children


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            node = HTMLNode(
                "p",
                children=text_to_children(block)
            )

            block_nodes.append(node)

        elif block_type == BlockType.HEADING:
            level = 0

            while block[level] == "#":
                level += 1

            heading_text = block[level + 1:]

            node = HTMLNode(
                f"h{level}",
                children=text_to_children(heading_text)
            )

            block_nodes.append(node)

        elif block_type == BlockType.CODE:
            code_text = block[4:-3]

            text_node = TextNode(
                code_text,
                TextType.CODE
            )

            code_node = text_node_to_html_node(text_node)

            pre_node = HTMLNode(
                "pre",
                children=[code_node]
            )

            block_nodes.append(pre_node)

        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")

            quote_lines = []

            for line in lines:
                quote_lines.append(
                    line[1:].lstrip()
                )

            quote_text = "\n".join(quote_lines)

            node = HTMLNode(
                "blockquote",
                children=text_to_children(quote_text)
            )

            block_nodes.append(node)

        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")

            items = []

            for line in lines:
                item_text = line[2:]

                item = HTMLNode(
                    "li",
                    children=text_to_children(item_text)
                )

                items.append(item)

            node = HTMLNode(
                "ul",
                children=items
            )

            block_nodes.append(node)

        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")

            items = []

            for line in lines:
                item_text = line.split(". ", 1)[1]

                item = HTMLNode(
                    "li",
                    children=text_to_children(item_text)
                )

                items.append(item)

            node = HTMLNode(
                "ol",
                children=items
            )

            block_nodes.append(node)

    return HTMLNode(
        "div",
        children=block_nodes
    )