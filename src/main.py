from textnode import TextNode, TextType
import shutil
import os

def clear_public_folder(): # + function to clear public folder directory and remove subdirectories
    print("****** attempting to delete public **********")
    shutil.rmtree(path = "./public")
    print("public folder deleted")
    pass

def initialize_public_folder(): # function to copy static to public
    print("getting dir list:")
    base_directory = "./static" # starting point for list
    
    print("calling get_list_files (recursive)")
    print(get_list_files(base_directory))

    pass

def get_list_files(parent_directory):
    stored_file_list = []
    #print(f"get_list_files recieved: {parent_directory}")
          
    if os.path.isdir(parent_directory): # if directory is incoming
        #print("os.path.isdir true")
        list_holder = os.listdir(parent_directory) # create list of that directory
        #print(f"created list: {list_holder}")

        for item in list_holder: 
            #print(f"iterating through list: {list_holder}, on item: {item}")

            joined = os.path.join(parent_directory, item)
            #print(f"joined: {joined}")

            if os.path.isfile(joined): # found item case
                #print(f"found item: {joined}")
                stored_file_list.append(joined)
            else: # found directory
                #print(f"found dir: {joined}")
                stored_file_list.extend(get_list_files(joined))
    else:
        #print(f"os.path.isdir false")
        stored_file_list.append(parent_directory)
    return stored_file_list

            
    """ old cludgy code
    for files in parent_directory:
        print(f"trying to list dir of: {files}")
        try:
            path = "./static" + current_filepath + "/" + files
            print(f"path is: {path}")

            file_holder = os.listdir(path) # trys getting file listing
            print(f"successfully stored {file_holder}, calling recursive")
            stored_file_list.extend(get_list_files(file_holder, current_filepath + '/' + files))
        except:
            print(f"failed to list contents of {files}, must be file, adding to list and returning")
            stored_file_list.append(current_filepath + '/' + files) # stores full filepath, adding filename to end
    return stored_file_list
    """

def main():
    testingnode = TextNode("my text", TextType.BOLD, "http://www.url.com")


    # clear_public_folder() working, commented out while testing for now
    print("calling initialize_public_folder")
    initialize_public_folder()

    # print(testingnode)
    pass


main ()