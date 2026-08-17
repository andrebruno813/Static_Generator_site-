from split_nodes_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType
import unittest


class TestSplit(unittest.TestCase):

    def test_bold(self):
        node = TextNode(
            "This is **bold** text",
            TextType.TEXT
        )

        result = split_nodes_delimiter(
            [node],
            "**",
            TextType.BOLD
        )

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_italic(self):
        node = TextNode(
            "This is _italic_ text",
            TextType.TEXT
        )

        result = split_nodes_delimiter(
            [node],
            "_",
            TextType.ITALIC
        )

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_code(self):
        node = TextNode(
            "This is `code` text",
            TextType.TEXT
        )

        result = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE
        )

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_multiple_bold(self):
        node = TextNode(
            "This is **bold** and **more bold**",
            TextType.TEXT
        )

        result = split_nodes_delimiter(
            [node],
            "**",
            TextType.BOLD
        )

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
        ]

        self.assertEqual(result, expected)

    def test_no_delimiter(self):
        node = TextNode(
            "This is normal text",
            TextType.TEXT
        )

        result = split_nodes_delimiter(
            [node],
            "**",
            TextType.BOLD
        )

        expected = [
            TextNode("This is normal text", TextType.TEXT)
        ]

        self.assertEqual(result, expected)

    def test_existing_non_text_node(self):
        node = TextNode(
            "already bold",
            TextType.BOLD
        )

        result = split_nodes_delimiter(
            [node],
            "**",
            TextType.BOLD
        )

        expected = [
            TextNode("already bold", TextType.BOLD)
        ]

        self.assertEqual(result, expected)

    def test_multiple_nodes(self):
        nodes = [
            TextNode("Hello **world**", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode(" and `code`", TextType.TEXT),
        ]

        result = split_nodes_delimiter(
            nodes,
            "**",
            TextType.BOLD
        )

        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode("already bold", TextType.BOLD),
            TextNode(" and `code`", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_unmatched_delimiter(self):
        node = TextNode(
            "This is **bold text",
            TextType.TEXT
        )

        with self.assertRaises(Exception):
            split_nodes_delimiter(
                [node],
                "**",
                TextType.BOLD
            )


if __name__ == "__main__":
    unittest.main()