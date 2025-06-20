from textnode import *
from file_ops import * # handles getting folder listings, clearing public, copying files, etc
import shutil
import os
import sys

def main():
    print("Current working directory:", os.getcwd())
        
    # Change to the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Gets the src directory
    project_dir = os.path.dirname(script_dir)  # Gets the project root
    os.chdir(project_dir)  # Change to project directory
    print("Changed working directory to:", os.getcwd())
    
    #testingnode = TextNode("my text", TextType.BOLD, "http://www.url.com")

    #print("calling initialize_public_folder")
    #initialize_public_folder()

    # print(testingnode)
    #print("testing extract_title():")
    
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
    
    basepath = "/"
    try: 
        if sys.argv[1] != "":
            basepath = sys.argv[1]
    except:
        pass
    

    #print(extract_title(test_md))
    #clear_public_folder() 
    static_directory = "./static" 

    file_list = get_list_files(static_directory) 
    copy_list_files(file_list) # copys over statics resources to public

    #from_path = "content/index.md" # from old direct call to generate_page
    #dest_path = "public/index.html" # from old direct call to generate_page

    dir_path_content = "content"
    template_path = "template.html"
    #dest_dir_path = "public"
    dest_dir_path = "docs"
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath)

main ()