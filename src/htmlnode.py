class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag #string ie "p", "a", "h1", etc
        self.value = value #value of the tag e.g. the texxt inside a paragraph
        self.children = children #LIST of HTMLNode objects representing the chilren of this node
        self.props = props #dictionary of key/value pairs of attribs
            # a link (<a> tag) might have {"href": "https://www.google.com"}
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self): #feeling good about this
        if self.props is None: #checks for none/missing dictionary
            return "" #ensures consistant behavior
        
        string_to_return = []
        unpacked_dict = self.props.items() #unpacks dictionary into a list of TUPLES

        for key, values in unpacked_dict: #goes through each tuple, reformatting and appending
            new_pair = f"{key}=\"{values}\""
            string_to_return.append(new_pair) 
        string_to_return = ' '.join(string_to_return)

        return ' ' + string_to_return #ensures leading space
    
    def __repr__(self):
        return f"tag: {self.tag} value: {self.value} children: {self.children} props: {self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, attributes=None):
        super().__init__(tag, value, children=None)
        self.attributes = attributes or {}

    def to_html(self):
            if self.value is None:
                raise ValueError("LeafNode must have a value")
            if self.tag is None:
                return self.value

            string_to_return = []
            attribute_pairs = self.attributes.items() #unpacks dictionary into a list of TUPLES
            for key, values in attribute_pairs: #goes through each tuple, reformatting and appending
                new_pair = f"{key}=\"{values}\""
                string_to_return.append(new_pair) 

            joined_string_to_return = f"{' '.join(string_to_return)}" #joins list of reformatted tuples
            if joined_string_to_return: #checks if there are a joined string of attributes, and adds a space if needed.
                joined_string_to_return = f" {joined_string_to_return}"
            
            attributes_string = f"<{self.tag}{joined_string_to_return}>{self.value}</{self.tag}>" #formats string   
            return attributes_string
    
class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__() #initiates in parent class
        self.tag = tag
        self.children = children if children is not None else [] #checks if children is empty, creates empty dictionary if missing
        self.props = props if props is not None else {} #assigns empty dictionary if props is empty
             
        if self.tag is None:
            raise ValueError("Required tag missing from parent node")
   
    def to_html(self):
        children_html = "" # will store children nodes in html format
        combined_props = "" # will store aditional key value props if present

        for key, value in self.props.items(): # items function neccessary to extract dictionary to key value paairs
            if key and value: # ennsures both key and value are present
                combined_props += f' {key}="{value}"'

        for child in self.children:
            children_html += (child.to_html())
        return f"<{self.tag}{combined_props}>{children_html}</{self.tag}>"