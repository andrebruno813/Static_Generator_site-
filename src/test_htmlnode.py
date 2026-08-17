import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        node = HTMLNode(
            tag="a",
            value="Google",
            props={
                "href":"https://www.google.com",
                "target":"_blank",
            },

        )
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"') 

    def test_empty_props(self):

        node = HTMLNode(
            tag="p",
            value="Hello",
            props={},
        )

        #assert node.props_to_html() == ""
        self.assertEqual(node.props_to_html(), "")

    def test_none_props(self):

        node = HTMLNode(
            tag="p",
            value="Hello",
        )

        self.assertEqual(node.props_to_html(), "") 
        #node.props_to_html() == ""