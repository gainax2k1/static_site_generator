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
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
            if self.value is None:
                raise ValueError("LeafNode must have a value")
            if self.tag is None:
                return self.value
            props_string = self.props_to_html()
    
            attributes_string = f"<{self.tag}{props_string}>{self.value}</{self.tag}>" #formats string   
            return attributes_string
    
class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag=tag, children=children, props=props)
        self.children = children if children is not None else [] #checks if children is empty, creates empty dictionary if missing
    
        if self.tag is None:
            raise ValueError("Required tag missing from parent node")
   
    def to_html(self):
        children_html = "" # will store children nodes in html format
        for child in self.children:
            children_html += child.to_html()
        
        props_string = self.props_to_html()
        
        return f"<{self.tag}{props_string}>{children_html}</{self.tag}>"
