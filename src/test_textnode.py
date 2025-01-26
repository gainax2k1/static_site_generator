import unittest

from textnode import *
from htmlnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node3 = TextNode("My very special text node", TextType.ITALIC, "http://www.url.com")   
        node4 = TextNode("yet another text node", TextType.ITALIC)
        node5 = TextNode("generic text node", TextType.LINK, "http://www.yourl.com")
        node6 = TextNode("my generic filler text node", TextType.IMAGE)
	
        test_split  = TextNode("hello `world` today", TextType.TEXT)
        delim_result = split_nodes_delimiter([test_split], "`", TextType.CODE)
        # Should result in 3 nodes: text, code, text 
        print(f"delim_result for test_split:'\n {delim_result}")

        #test_split2 = TextNode("Boots is the ** bestest ** bear * ever *!", TextType.TEXT)
        #delim_result2 = split_nodes_delimiter([test_split2],  "**", TextType.BOLD)# "[]" list of list nodes
        #print(f"delim_result for test_split2:'\n {delim_result2}")
        #delim_result3 = split_nodes_delimiter(delim_result2,  "*", TextType.ITALIC)# no "[]" because already list of nodes
        #print(f"delim_result for test_split3:'\n {delim_result3}")     


        test_split2 = TextNode("Boots is the ** bestest ** bear * ever *!", TextType.TEXT)
        
        # Test bold split first
        delim_result2 = split_nodes_delimiter([test_split2], "**", TextType.BOLD)
        assert len(delim_result2) == 3  # Should be: text, bold, text
        assert delim_result2[0].text == "Boots is the "
        assert delim_result2[0].text_type == TextType.TEXT
        assert delim_result2[1].text == " bestest "
        assert delim_result2[1].text_type == TextType.BOLD
        assert delim_result2[2].text == " bear * ever *!"
        assert delim_result2[2].text_type == TextType.TEXT
        print(f"delim_result for test_split2:'\n {delim_result2}")
        
        # Test italic split on the result
        delim_result3 = split_nodes_delimiter(delim_result2, "*", TextType.ITALIC)
        assert len(delim_result3) == 5  # Should now be: text, bold, text, italic, text
        assert delim_result3[3].text == " ever "
        assert delim_result3[3].text_type == TextType.ITALIC
        print(f"delim_result for test_split3:'\n {delim_result3}")

        test_text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        print(test_text)
        print(extract_markdown_links(test_text))
        # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

        print("Now testing split image links")
        link_node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
            )
        new_nodes = split_nodes_link([link_node])
        print(new_nodes)

        print("now testing text to textnodes")
        text_to_test = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        print(text_to_test)
        print(text_to_textnodes(text_to_test))

        print("test split blocks:")

        test_md = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it. 

        * This is the first list item in a list block
        * This is a list item
        * This is another list item

        ```this is code text```

        > list in block
        > list in blockk
        > list in blockkk

        1. first item
        2. second item
        3. third item
        """
        print(f"test_md = {test_md}")

        blocks_list = markdown_to_blocks(test_md)
        print(blocks_list)

        print("testing block types:")
        for block in blocks_list:
            print(f"testing {block}:")
            print(block_to_block_type(block))

        print("testing markdown_to_html_node")
        print(markdown_to_html_node(test_md))
        


if __name__ == "__main__":
    unittest.main()
