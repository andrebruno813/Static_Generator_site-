#from textnode import TextNode, TextType
import os
import shutil

dir_path_static = "./static"
dir_path_public = "./public"

def copy_fyles_recursive(source_dir_path: str, dest_dir_path: str) -> None:
    
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    
    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")

        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_fyles_recursive(from_path, dest_path)

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    
    print("Copying static files to public directory...")
    copy_fyles_recursive(dir_path_static, dir_path_public)

if __name__ == "__main__":
    main()