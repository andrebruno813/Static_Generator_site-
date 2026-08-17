import unittest

from markdown_extract import (
    extract_markdown_images,
    extract_markdown_links,
)


class TestMarkdownExtract(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )

        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches
        )

    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "![cat](cat.png) and ![dog](dog.png)"
        )

        self.assertListEqual(
            [
                ("cat", "cat.png"),
                ("dog", "dog.png"),
            ],
            matches
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a [link](https://example.com)"
        )

        self.assertListEqual(
            [("link", "https://example.com")],
            matches
        )

    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "[Google](https://google.com) and [Boot.dev](https://boot.dev)"
        )

        self.assertListEqual(
            [
                ("Google", "https://google.com"),
                ("Boot.dev", "https://boot.dev"),
            ],
            matches
        )

    def test_image_is_not_link(self):
        matches = extract_markdown_links(
            "This is an ![image](https://example.com/image.png)"
        )

        self.assertListEqual([], matches)

    def test_no_images(self):
        matches = extract_markdown_images(
            "This text has no images"
        )

        self.assertListEqual([], matches)

    def test_no_links(self):
        matches = extract_markdown_links(
            "This text has no links"
        )

        self.assertListEqual([], matches)


if __name__ == "__main__":
    unittest.main()