import unittest
import htmlnode
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        htmlnode = HTMLNode("a", "textforinside", None, {"href": "https://www.testurl.com"})
        print(htmlnode.props_to_html())

        htmlnode2 = HTMLNode("a", "different inside", None, {"href": "https://example.com", "target": "_blank"})
        print(htmlnode2.props_to_html())

        htmlnode3 = HTMLNode("a", "fillerfiler", None, {}) 
        print(htmlnode3.props_to_html())

        htmlnode4 = HTMLNode("a", "generictext", None, {"id": "main", "class": "container"})
        print(htmlnode4.props_to_html())

        print(f"htmlnode: {htmlnode}")
        print(f"htmlnode2: {htmlnode2}")
        print(f"htmlnode3: {htmlnode3}")
        print(f"htmlnode4: {htmlnode4}")

        leafnode1 = LeafNode("p", "This is a paragraph of text.")
        leafnode2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        print(leafnode1)
        print(leafnode1.to_html)
        print(leafnode2)
        print(leafnode2.to_html) 

        print("testing parent/leafs:")

        nodeparent = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        print(nodeparent.to_html())

        pass


if __name__ == "__main__":
    unittest.main()
