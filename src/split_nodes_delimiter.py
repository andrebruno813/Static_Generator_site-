from textnode import TextNode
from textnode import TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    
    new_nodes = []

    for old_node in old_nodes:

        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        parts = old_node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception("Invalid Markdown: unmatched delimiter")

        for i, part in enumerate(parts):

            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
                
    return new_nodes

