import unittest

from markdown_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_block(self):
        md = "This is a paragraph"

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is a paragraph"
            ],
        )

    def test_multiple_blocks(self):
        md = """# Heading

Paragraph

- item 1
- item 2"""

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Paragraph",
                "- item 1\n- item 2",
            ],
        )

    def test_empty_blocks(self):
        md = """# Heading


Paragraph"""

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Paragraph",
            ],
        )

    def test_leading_and_trailing_whitespace(self):
        md = """

# Heading

Paragraph

"""

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Paragraph",
            ],
        )


if __name__ == "__main__":
    unittest.main()