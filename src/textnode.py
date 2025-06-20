from enum import Enum
from htmlnode import *
from file_ops import * # handles getting folder listings, clearing public, copying files, etc
import re #regex
import os
import shutil

class TextType(Enum):
	TEXT = "TEXT"      # was "normal"
	BOLD = "BOLD"      # was "bold"
	BLOCKQUOTE = "BLOCKQUOTE" # was "blockquote"
	ITALIC = "ITALIC"  # was "italic"
	CODE = "CODE"      # was "code"
	LINK = "LINK"      # was "links"
	IMAGE = "IMAGE"    # was "images"


class MarkdownParsingError(Exception):
    pass

class TextNode():
	def __init__(self, text, text_type, url=None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, value): # defines "=" for TextNode instances
		if self.text == value.text and self.text_type == value.text_type and self.url == value.url:
			return True
		return False
	
	def __repr__(self): # defines how to print instance of TextNode ( so print(my_text_node) works
		return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
	
	def to_html(self):
		if self.text_type == TextType.TEXT:
			return self.text
		elif self.text_type == TextType.BOLD:
			return f"<b>{self.text}</b>"
		elif self.text_type == TextType.ITALIC:
			return f"<i>{self.text}</i>"
		elif self.text_type == TextType.CODE:
			return f"<code>{self.text}</code>"
		elif self.text_type == TextType.LINK:
			return f"<a href=\"{self.url}\">{self.text}</a>"
		elif self.text_type == TextType.IMAGE:
			return f"<img src=\"{self.url}\" alt=\"{self.text}\">"
		else:
			raise ValueError(f"Invalid text type: {self.text_type}")
	
def text_node_to_html_node(text_node): # receives object of type text node, formats with tags
	print(f"Converting node: {text_node}")

	match text_node.text_type:
		case TextType.TEXT:
			if text_node.text is None:
				raise ValueError("PLAIN_TEXT Node has no text")
			return LeafNode(tag=None, value=text_node.text)
			# Create a plain text LeafNode

		case TextType.BOLD:
			if text_node.text is None:
				raise ValueError("BOLD_TEXT Node has no text")
			return LeafNode(tag="b", value=text_node.text)
			# Create a LeafNode for bold text

		case TextType.BLOCKQUOTE:
			if text_node.text is None:
				raise ValueError("BLOCKQUOTE_TEXT Node has no text")
			return LeafNode(tag="<blockquote>", value=text_node.text)
			# Create a LeafNode for bold text

		case TextType.ITALIC:
			if text_node.text is None:
				raise ValueError("ITALIC_TEXT Node has no text")
			return LeafNode(tag="i", value=text_node.text)
			# Create a LeafNode for italic text

		case TextType.CODE:
			if text_node.text is None:
				raise ValueError("CODE_TEXT Node has no text")
			return LeafNode(tag="code", value=text_node.text)
			# Create a LeafNode with props for a code segment

		case TextType.LINK:
			if text_node.text is None:
				raise ValueError("LINK Node has no text")
			if text_node.url is None:
				raise ValueError("LINK Node missing URL")			
			return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url}) #props as key/value
			# Create a LeafNode with props for a hyperlink

		case TextType.IMAGE:
			if text_node.text is None:
				raise ValueError("IMAGE Node has no ALT text")
			if text_node.url is None:
				raise ValueError("IMAGE Node missing SRC URL")		
			return LeafNode(tag="img", value=text_node.text, props={"src": text_node.url, "alt":text_node.text}) #props as key/value
			# Create a LeafNode with props for an image

		case _:
			# Raise an exception for unhandled types
			raise ValueError(f"Unhandled TextType: {text_node.type}")	

def split_nodes_delimiter(old_nodes, delimiter, text_type):  #takes in TextNode list, delimter (ie, "'"),
	# and text type for within the delimeter (ie, TextType.CODE)
	print(f"Processing delimiter '{delimiter}' for nodes:")
	delimited_text = [] #to store all the nodes after delimitation
	for each_node in old_nodes: 
		if each_node.text_type is not TextType.TEXT: #checks to see if it's a text node, if not, moves on.
			delimited_text.append(each_node) #appends node unchanged
			continue #skips rest of this iteration, goes back to top of for loop

		temp_text = each_node.text #temporarily holds value of eachnode.text for this iteration
		first_delim = temp_text.find(delimiter) #looks for first instance of delimeter in this part

		if first_delim == -1:  # if no istance of the delimeter is found
			delimited_text.append(each_node) # If no delimiter found, keep this node unchanged
			continue # skips rest of this iteration, goes back to top of for loop

		second_delim = temp_text.find(delimiter, first_delim + len(delimiter)) #starts search after first delimeter
		if second_delim == -1: # Found opening delimiter but no closing one, like "text `code without end"
			raise ValueError(f"No closing delimiter '{delimiter}' found")
		
		## Now we have starting and ending points of the text to delimit, no we're forming it ***\
		before_text = temp_text[:first_delim] # Text before the first delimite
		if before_text:
			delimited_text.append(TextNode(before_text, TextType.TEXT))

		between_text = temp_text[first_delim + len(delimiter):second_delim] # Text between delimiters
		delimited_text.append(TextNode(between_text, text_type))
        
		after_text = temp_text[second_delim + len(delimiter):] # Text after the second delimiter
		if after_text: # only trys to append if there's more text after the delimination
			#delimited_text.append(TextNode(after_text, TextType.TEXT))
			remaining_nodes = split_nodes_delimiter([TextNode(after_text, TextType.TEXT)], delimiter, text_type)
			delimited_text.extend(remaining_nodes)


		#end of loop, back to top
		print(f"Found delimiters at positions: {first_delim}, {second_delim}")
	return delimited_text #list of delimited nodes

def extract_markdown_images(text): # takes raw markdown text and returns a list of tuples.
	# Each tuple should contain the alt text and the URL of any markdown images

	# abstracted_image_tuples = re.findall(r"!\[(.*?)\]\((.*?)\)", text) # my version
		# !\[ - match literal ![
		# (.*?) - CAPTURE any characters until...
		# \] - we hit the closing bracket
		# \( - match literal (
		# (.*?) - CAPTURE any characters until...
		# \) - we hit the closing parenthesis
		# Output: [('cat', 'cat.jpg'), ('dog', 'dog.jpg')]

	return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text): #extracts markdown links instead of images. 
	# It should return tuples of anchor text and URLs
	# insert more smartypants code here, it'll prolly be very similar to above

	# abstracted_link_tuples = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text) # my vers. like above, BUT:
		# (?<!!) - "make sure there ISN'T a ! before this position"
		# (?<! ... ) - This is the syntax for "negative lookbehind"
		#    (?<! - starts the negative lookbehind
		#    ! - the character we're checking for
		#    ) - ends the lookbehind

	return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes): # takes in a list of nodes, converts to split text nodes
	split_image_nodes_to_return = []  # creates list to store new node list to return

	for each_node in old_nodes: # going through each old node
		extracted_md_images = extract_markdown_images(each_node.text) 
		if not extracted_md_images: #checks to see if there is an imagenode, if not, moves on.
			if each_node.text == "": 
				continue
			split_image_nodes_to_return.append(each_node) #appends old node unchanged
			continue #skips rest of this iteration, goes back to top of for loop

		alt_text, url = extracted_md_images[0]  # Unpack the tuple
		markdown_delimiter = f"![{alt_text}]({url})" # now checked, ok to build
		temp_text = each_node.text #temporarily holds value of original old node.text for this iteration
		split_image_text = temp_text.split(markdown_delimiter, 1) # splits at MD
		
		if len(split_image_text) < 2:
			split_image_text.append("")  # Ensure we have two elements in split_image_text

		# Append valid TextNodes
		if split_image_text[0]:  # Skip if the leading text is empty
			split_image_nodes_to_return.append(TextNode(split_image_text[0], TextType.TEXT))
		split_image_nodes_to_return.append(TextNode(alt_text, TextType.IMAGE, url))
		if split_image_text[1]:  # Skip if the trailing text is empty
			split_image_nodes_to_return.append(TextNode(split_image_text[1], TextType.TEXT))
	return split_image_nodes_to_return

def split_nodes_link(old_nodes): # basically same logic as above, but for links instead of images
	split_link_nodes_to_return = []  # creates list to store new node list to return

	for each_node in old_nodes: # going through each old node
		extracted_md_link = extract_markdown_links(each_node.text)
		if not extracted_md_link: #checks to see if there is an imagenode, if not, moves on.
			if each_node.text == "": 
				continue
			split_link_nodes_to_return.append(each_node) #appends old node unchanged
			continue #skips rest of this iteration, goes back to top of for loop
		
		link_text, url = extracted_md_link[0]  # Unpack the tuple
		markdown_delimiter = f"[{link_text}]({url})" # now checked, ok to build
		temp_text = each_node.text #temporarily holds value of original old node.text for this iteration
		split_link_text = temp_text.split(markdown_delimiter, 1) # splits at MD
		if len(split_link_text) < 2:
			split_link_text.append("")  # Ensure we have two elements in split_link_text
			
		# Append valid TextNodes
		if split_link_text[0]:  # Skip if the leading text is empty
			split_link_nodes_to_return.append(TextNode(split_link_text[0], TextType.TEXT))
		split_link_nodes_to_return.append(TextNode(link_text, TextType.LINK, url))
		if split_link_text[1]:  # Skip if the trailing text is empty
			split_link_nodes_to_return.append(TextNode(split_link_text[1], TextType.TEXT))
	return split_link_nodes_to_return

def text_to_textnodes(text): # takes markdown document, determines each type, creates text nodes for each piece
	nodes = [TextNode(text, TextType.TEXT)] # starting node is entire contents, marked as TEXT
	split_image = split_nodes_image(nodes) # goes through first node, spliting at image tags
	split_link = split_nodes_link(split_image) # takes processed list of nodes from previous, splitting at link tags
	split_bold = split_nodes_delimiter(split_link, "**", TextType.BOLD) # and so on...
	split_italic = split_nodes_delimiter(split_bold, "*", TextType.ITALIC)
	split_italic2 = split_nodes_delimiter(split_italic, "_", TextType.ITALIC)
	split_code = split_nodes_delimiter(split_italic2, "`", TextType.CODE)
	split_blockquote = split_nodes_delimiter(split_code, ">", TextType.BLOCKQUOTE)
	return split_blockquote # shouldl be list of fully type demarkated nodes

def markdown_to_blocks(markdown): #markdown is one large text
	rough_blocked_md = markdown.split("\n\n")
	blocks_to_return = []
	for block in rough_blocked_md:
        # Split block into lines, strip each line, then rejoin
		lines = [line.strip() for line in block.split('\n')]
		temp_block = '\n'.join(lines)
		if len(temp_block) == 0:
			continue
		blocks_to_return.append(temp_block)

	return blocks_to_return

def block_to_block_type(md_text): #single blcok of markdown text input, returns string representing type of block
	if re.match("^#{1,6}\s.+", md_text): #Check for heading #s (^ = begining of string, #{1,6} = 1-6 #s, \s = space, .+ = any number of characters
		return "heading"
	if re.match("(?s)^`{3}.+`{3}$", md_text): # ^ - start of string, `{3} = 3`, (/s).+ = any content, inculding new line, `{3}$ = 3` at end of line
		return "code"
	lines = [line for line in md_text.split('\n') if line]
	# OLD VERSION : lines = md_text.split('\n') # splits md_text into lines to check if each line begins with character for lists
	#print(f"\nDEBUG - Processing block: {md_text}")
	#print(f"DEBUG - Split into lines: {lines}")

	#print("DEBUG - Checking quote...")
	if all(line.startswith('>') for line in lines):
		return "blockquote"
	#print("DEBUG - Checking unordered list...")
	if all(line.startswith('* ') or line.startswith('- ') for line in lines):
		return "unordered_list"
	#print("DEBUG - Checking ordered list...")
	for i, line in enumerate(lines, 1): # loops through the enumerated list, to make sure the leading number goes in proper 1, 2, 3.. order, and not 3,1,5... or whatever
		#print(f"DEBUG - Checking line {i}: '{line}'")
		if not line.startswith(f"{i}. "):
			#print(f"DEBUG - Failed at line {i}") 
			break #fails the number check, breaks out of the for loop altogether
	else:  # This runs if we never hit break
		if len(lines) > 0:  # Make sure it's not empty
			return "ordered_list"
	
	#print("DEBUG - Defaulting to paragraph")
	return "paragraph" # default, if nothing else matched

def markdown_to_html_node(markdown): # converts full md doc into a single PARENT HTMLNode
	split_blocks = markdown_to_blocks(markdown)
	parent_node = ParentNode(tag="div", children=[])

	for block in split_blocks:
		block_type = block_to_block_type(block)
		
		match block_type: # assuming single blocktype per block
			case "blockquote":
				block_node = md_blockquote(block)
			case "unordered_list":
				block_node = md_unordered_list(block)
			case "ordered_list":
				block_node = md_ordered_list(block)
			case "code":
				block_node = md_code(block)
			case "heading":
				block_node = md_heading(block)
			case "paragraph":
				block_node = md_paragraph(block)
			case _:
				raise MarkdownParsingError(f"Unknown block type: {block}")
		if not block_node: # in cases where
			continue
		parent_node.children.append(block_node)  # correct
	return parent_node

""" PSEUDO CODE:
# 1). Split md into blocks (use markdown_to_blocks)
# 2). Loop over each block-
#	-Determine block type (block_to_block_type)
#	-based on block type, create new HTMLNode with proper data
# 	-Assign propper child HTMLNode objects to the block node (use text_to_children )
# 3) Make all the block nodes children under single parent node (which should just be a <div>) and return it.
"""

def md_blockquote(md_text): # + places blockquote tags
	split_md_text = md_text.split('\n')
	clean_content = ""

    # Your existing cleaning logic
	for line in split_md_text:
		if line.strip():
			if line.startswith(">"):
				content = line[1:].strip()
			else:
				content = line
			clean_content += content + "\n"
	clean_content = clean_content.rstrip("\n")
    
	 # Process content for inline formatting
	text_nodes = text_to_textnodes(clean_content)
	child_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
    # Return a LeafNode instead
	return ParentNode(tag="blockquote", children=child_nodes)

def md_unordered_list(md_text): # + places ul tags
	if not md_text.strip():
		return ""
	split_md_text = md_text.split('\n')
	list_items = []  # Will hold our LeafNodes for each list item
	for line in split_md_text:
		if line.strip():
			if line.startswith("*") or line.startswith("-"):
				content = line[1:].strip()
				text_nodes = text_to_textnodes(content)
				# Convert text nodes to HTML strings and join them
				child_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
				list_items.append(ParentNode(tag="li", children=child_nodes))
    # Create a ParentNode for the ul that contains all list items
	return ParentNode(tag="ul", children=list_items)

def md_ordered_list(md_text): # + places ordered list tags
	"""
    Converts a Markdown ordered list block to an HTML ordered list (<ol>) structure.

    Args:
        md_text (str): The Markdown text containing an ordered list.

    Returns:
        str: An HTML ordered list as a string, or an empty string for empty input.

    Raises:
        ValueError: If any line does not match the ordered list format.
    """
	if not md_text.strip():
		return ""  # Return nothing for empty input

	split_md_text = md_text.split('\n') # split block into lines
	list_items = []

	for line in split_md_text: #  going trough each line of block
		if line.strip(): # ignore empty lines
			match = re.match(r"^\d+[.)]\s+(.+)", line)
			if match: # This matches numbers (one or more digits),
				# followed by either a . or ), followed by at least one space, and then the item's content.
				content = match.group(1).strip()
				text_nodes = text_to_textnodes(content)

				# Convert text nodes to HTML nodes
				child_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
				# Create a parent node for the list item
				list_items.append(ParentNode(tag="li", children=child_nodes))
			else:
				raise ValueError("Unexpected unnumbered line {line} in ordered list.")  # Optional strictness

	return ParentNode(tag="ol", children=list_items)

def md_code(md_text): # + marks code tags
	stripped = md_text.strip()
	if stripped.startswith("```") and stripped.endswith("```"):

		if "\n" in md_text.strip(): # multi-line
			# Strip only the first and last lines containing ```
			lines = md_text.split("\n")
			content_lines = lines[1:-1]  # Everything except the first and last lines
			stripped_md_text = "\n".join(content_lines).strip()  # Join the code and remove extra whitespace
			if stripped_md_text == "": # in case there was nothing between md code, returns nothing
				return ""
		else: # single line
			stripped_md_text = md_text.strip('`').strip()
			if stripped_md_text == "":
				return ""	
		code_node = LeafNode(tag="code", value=stripped_md_text)
		return ParentNode(tag="pre", children=[code_node])
	if stripped.startswith("`") and stripped.endswith("`"):
		stripped_md_text = md_text.strip('`').strip()
		return LeafNode(tag="code", value=stripped_md_text) 
	else:
		raise ValueError(f"Input {md_text} is not a valid Markdown code block.")


def md_heading(md_text): # +  marks heading, depending on number of #
	heading_size = 0
	for char in md_text:
		if char == "#":
			heading_size += 1
		else:
			break
	if heading_size < 1 or heading_size > 6:
		raise ValueError (f"invalid heading size of: {heading_size}")
				   
	heading_text = md_text[heading_size:].strip()
	if not heading_text:
		raise ValueError(f"# characters not followed by valid content in {md_text}")
	content = md_text.lstrip('#').strip()
	text_nodes = text_to_textnodes(content)
	#formatted_content = "".join([node.to_html() for node in text_nodes])
	#return LeafNode(tag=f"h{heading_size}", value=formatted_content)
	child_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
	return ParentNode(tag=f"h{heading_size}", children=child_nodes)

def md_paragraph(md_text): # + marks paragraph tags
	# First get the TextNodes for any inline formatting
	text_nodes = text_to_textnodes(md_text)
	# Convert TextNodes to HTMLNodes
	child_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
	# Create paragraph as ParentNode with the child nodes		
	return ParentNode(tag="p", children=child_nodes)

def extract_title(markdown): # pull h1 header from md file
	if not markdown: # empty string
		raise Exception("No title found to extract")
	split_md_text = markdown.split('\n')

	if not split_md_text[0].startswith("# "):
		raise Exception("No title found to extract")
	
	first_line = split_md_text[0].lstrip('# ') #  removes leading "# " from line only
	return first_line

def generate_page(from_path, template_path, dest_path, basepath): # generates html from md
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")
	
	os.makedirs(os.path.dirname(dest_path), exist_ok=True) # Create directory if it doesn't exist

	with open(from_path, 'r') as md_file: # opens from_path as read, ref as md_file
		markdown_content = md_file.read() # reads data from md_file, stores it in markdown_content, 
	
	with open(template_path, 'r') as template_file: # opens from template_path as read, ref as template_file
		template_content = template_file.read() # reads date from template_file, stores it in template content.

	converted_md_to_html = markdown_to_html_node(markdown_content)
	html_string = converted_md_to_html.to_html()
	title = extract_title(markdown_content)

	template_content = template_content.replace("{{ Title }}", title)
	template_content = template_content.replace("{{ Content }}", html_string)
	template_content = template_content.replace('href="/', f'href="{basepath}')
	template_content = template_content.replace('src="/', f'src="{basepath}')
	
	with open(dest_path, 'w') as output_file: # opens dest_path as write, ref as output_file
		output_file.write(template_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath): # crawls everything in content dir
	# For each md file found, generate .html file using same *template.html*. Write generated pages to public

	content_list = get_list_files(dir_path_content)

	# Filter for only markdown files here
	markdown_files = [f for f in content_list if f.endswith('.md')]

	for md_file in markdown_files:
		relative_path = os.path.relpath(md_file, "content") # strips 'content' from the file path

		# os.path.splitext splits the path into ('majesty/index', '.md'), for example
    	# We take [0] to get 'majesty/index' and add '.html'
		html_path = os.path.splitext(relative_path)[0] + ".html"  # Change the extension from .md to .html
		destination = os.path.join(dest_dir_path, html_path) # puts "public" where  'content' was in file path

		generate_page(md_file, template_path, destination, basepath) # generates the "md_file"

