from enum import Enum

class BlockType(Enum):

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):

    # HEADING

    for i in range(1, 7):
        if block.startswith("#" * i + " "):
            return BlockType.HEADING
    
    # CODE

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split("\n")

    # QUOTE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    # UNORDERED LIST
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    # ORDERED LIST
    for i, line in enumerate(lines):
        expected = f"{i + 1}. "

        if not line.startswith(expected):
            break
    else:
        return BlockType.ORDERED_LIST
    
    # PARAGRAPH
    return BlockType.PARAGRAPH

    

