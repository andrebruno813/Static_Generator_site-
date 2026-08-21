import unittest

from blocktype import BlockType, block_to_block_type


class TestBlockType(unittest.TestCase):

    def test_heading(self):
        self.assertEqual(
            block_to_block_type("# Heading"),
            BlockType.HEADING,
        )

    def test_all_heading_levels(self):
        for i in range(1, 7):
            block = "#" * i + " Heading"

            self.assertEqual(
                block_to_block_type(block),
                BlockType.HEADING,
            )

    def test_invalid_heading(self):
        self.assertEqual(
            block_to_block_type("####### Heading"),
            BlockType.PARAGRAPH,
        )

        self.assertEqual(
            block_to_block_type("#Heading"),
            BlockType.PARAGRAPH,
        )

    def test_code(self):
        block = "```\nprint('hello')\nprint('world')\n```"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_quote(self):
        block = "> Hello\n> This is a quote\n> Another line"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_quote_without_space(self):
        block = ">Hello\n>World"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_invalid_quote(self):
        block = "> Hello\nThis is not a quote"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_unordered_list(self):
        block = "- First\n- Second\n- Third"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST,
        )

    def test_invalid_unordered_list(self):
        block = "- First\n-Second\n- Third"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST,
        )

    def test_ordered_list_must_start_at_one(self):
        block = "2. First\n3. Second"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_must_increment(self):
        block = "1. First\n3. Third"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_paragraph(self):
        block = "This is a normal paragraph."

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )


if __name__ == "__main__":
    unittest.main()