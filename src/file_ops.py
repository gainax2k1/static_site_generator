import shutil
import os

def clear_public_folder(): # + function to clear public folder directory and remove subdirectories
    print("****** attempting to delete public **********")
    if os.path.exists("./public"):
        shutil.rmtree("./public")
        print("public folder deleted")
    else:
        print("public folder doesn't exist yet")

def initialize_public_folder(): # function to copy static to public
    clear_public_folder() 
    print("public folder wiped, begining initialization")
    print("getting dir list:")
    base_directory = "./static" # starting point for list
    
    static_file_listing = get_list_files(base_directory)
    print("beginning to copy")
    copy_list_files(static_file_listing)

def get_list_files(parent_directory): # lists directory structure of given parent directory
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

def copy_list_files(file_list): #copys list of files from their source to "public"
    for item in file_list:
        print(f"copying item: {item} to public from: {file_list}")

        relative_path = os.path.relpath(item, "static") # strips the static from the path
        print(f"relative path: {relative_path}")
    
        destination = os.path.join("public", relative_path) # puts public in the path where static used to be
        print(f"destination: {destination}")
    
        destination_directory = os.path.dirname(destination) # gets just the directory part w/o the filename
        print(f"destination directory: {destination_directory}")
    
        os.makedirs(destination_directory, exist_ok=True) # makes all the neccessary directories, if needed
        print("directory made")

        print(f"copying item: {item} to public")
        shutil.copy(item, destination)


