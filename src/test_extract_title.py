import unittest

from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):

    def test_extract_title(self):
        markdown = "# Hello"

        self.assertEqual(
            extract_title(markdown),
            "Hello",
        )

    def test_extract_title_with_spaces(self):
        markdown = "#   Hello World   "

        self.assertEqual(
            extract_title(markdown),
            "Hello World",
        )

    def test_title_with_other_blocks(self):
        markdown = """
# Tolkien Fan Club

This is a paragraph.

## Another heading
"""

        self.assertEqual(
            extract_title(markdown),
            "Tolkien Fan Club",
        )

    def test_no_title(self):
        markdown = """
This is a paragraph.

## This is not an H1
"""

        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_h2_is_not_h1(self):
        markdown = "## Hello"

        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()