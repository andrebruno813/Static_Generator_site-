import unittest
from  split_nodes import (split_nodes_image , split_nodes_link)
from textnode import TextNode, TextType


class TestSplitNodes(unittest.TestCase):

    # =========================
    # IMAGES
    # =========================

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode(
                    "This is text with an ",
                    TextType.TEXT,
                ),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://i.imgur.com/zjjcJKZ.png",
                ),
            ],
            new_nodes,
        )

    def test_split_multiple_images(self):
        node = TextNode(
            "![one](one.png) and ![two](two.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("one", TextType.IMAGE, "one.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "two.png"),
            ],
            new_nodes,
        )

    def test_image_at_beginning(self):
        node = TextNode(
            "![image](image.png) is here",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "image.png"),
                TextNode(" is here", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_end(self):
        node = TextNode(
            "Here is ![image](image.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "image.png"),
            ],
            new_nodes,
        )

    def test_only_image(self):
        node = TextNode(
            "![image](image.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "image.png"),
            ],
            new_nodes,
        )

    def test_no_images(self):
        node = TextNode(
            "This is just normal text",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [node],
            new_nodes,
        )

    # =========================
    # LINKS
    # =========================

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode(
                    "This is text with a ",
                    TextType.TEXT,
                ),
                TextNode(
                    "link",
                    TextType.LINK,
                    "https://example.com",
                ),
            ],
            new_nodes,
        )

    def test_split_multiple_links(self):
        node = TextNode(
            "[Google](https://google.com) and [Boot](https://boot.dev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode(
                    "Google",
                    TextType.LINK,
                    "https://google.com",
                ),
                TextNode(
                    " and ",
                    TextType.TEXT,
                ),
                TextNode(
                    "Boot",
                    TextType.LINK,
                    "https://boot.dev",
                ),
            ],
            new_nodes,
        )

    def test_link_at_beginning(self):
        node = TextNode(
            "[Google](https://google.com) is a website",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode(
                    "Google",
                    TextType.LINK,
                    "https://google.com",
                ),
                TextNode(
                    " is a website",
                    TextType.TEXT,
                ),
            ],
            new_nodes,
        )

    def test_link_at_end(self):
        node = TextNode(
            "Visit [Google](https://google.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode(
                    "Visit ",
                    TextType.TEXT,
                ),
                TextNode(
                    "Google",
                    TextType.LINK,
                    "https://google.com",
                ),
            ],
            new_nodes,
        )

    def test_only_link(self):
        node = TextNode(
            "[Google](https://google.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode(
                    "Google",
                    TextType.LINK,
                    "https://google.com",
                ),
            ],
            new_nodes,
        )

    def test_no_links(self):
        node = TextNode(
            "This is just normal text",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [node],
            new_nodes,
        )

    # =========================
    # EXISTING NON-TEXT NODES
    # =========================

    def test_image_does_not_modify_non_text_nodes(self):
        node = TextNode(
            "already bold",
            TextType.BOLD,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [node],
            new_nodes,
        )

    def test_link_does_not_modify_non_text_nodes(self):
        node = TextNode(
            "already bold",
            TextType.BOLD,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [node],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()