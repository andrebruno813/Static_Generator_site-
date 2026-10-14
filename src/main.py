import os
import shutil
import sys

from markdown_to_html import markdown_to_html_node
from extract_title import extract_title


dir_path_static = "./static"
dir_path_output = "./docs"


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


def normalize_basepath(basepath: str) -> str:
    if basepath is None or basepath == "":
        return "/"

    if not basepath.startswith("/"):
        basepath = "/" + basepath

    if not basepath.endswith("/"):
        basepath += "/"

    return basepath


def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(
        f"Generating page from {from_path} "
        f"to {dest_path} using {template_path}"
    )

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()

    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    parent_dir = os.path.dirname(dest_path)

    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath="/"):
    for root, _, files in os.walk(dir_path_content):
        for filename in files:
            if not filename.endswith(".md"):
                continue

            from_path = os.path.join(root, filename)
            relative_dir = os.path.relpath(os.path.dirname(from_path), dir_path_content)
            relative_dest_dir = dest_dir_path if relative_dir == "." else os.path.join(dest_dir_path, relative_dir)
            dest_path = os.path.join(relative_dest_dir, os.path.splitext(filename)[0] + ".html")

            generate_page(from_path, template_path, dest_path, basepath)


def generate_pages(content_dir_path: str, template_path: str, dest_dir_path: str, basepath="/"):
    generate_pages_recursive(content_dir_path, template_path, dest_dir_path, basepath)


def main():
    basepath = normalize_basepath(sys.argv[1]) if len(sys.argv) > 1 else "/"

    print("Deleting output directory...")

    if os.path.exists(dir_path_output):
        shutil.rmtree(dir_path_output)

    print("Copying static files to output directory...")
    copy_fyles_recursive(dir_path_static, dir_path_output)

    generate_pages_recursive(
        "content",
        "template.html",
        dir_path_output,
        basepath,
    )


if __name__ == "__main__":
    main()