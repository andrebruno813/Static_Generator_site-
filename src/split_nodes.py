from textnode import TextNode, TextType
from markdown_extract import extract_markdown_images, extract_markdown_links


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:

        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        images = extract_markdown_images(original_text)

        if not images:
            new_nodes.append(old_node)
            continue

        for image_alt, image_url in images:
            markdown_image = f"![{image_alt}]({image_url})"

            sections = original_text.split(markdown_image, 1)

            if sections[0] != "":
                new_nodes.append(
                    TextNode(
                        sections[0],
                        TextType.TEXT
                    )
                )

            new_nodes.append(
                TextNode(
                    image_alt,
                    TextType.IMAGE,
                    image_url
                )
            )

            original_text = sections[1]

        if original_text != "":
            new_nodes.append(
                TextNode(
                    original_text,
                    TextType.TEXT
                )
            )

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:

        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        links = extract_markdown_links(original_text)

        if not links:
            new_nodes.append(old_node)
            continue

        for link_text, link_url in links:
            markdown_link = f"[{link_text}]({link_url})"

            sections = original_text.split(markdown_link, 1)

            if sections[0] != "":
                new_nodes.append(
                    TextNode(
                        sections[0],
                        TextType.TEXT
                    )
                )

            new_nodes.append(
                TextNode(
                    link_text,
                    TextType.LINK,
                    link_url
                )
            )

            original_text = sections[1]

        if original_text != "":
            new_nodes.append(
                TextNode(
                    original_text,
                    TextType.TEXT
                )
            )

    return new_nodes