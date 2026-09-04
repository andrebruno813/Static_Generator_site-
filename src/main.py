import os
import shutil

from markdown_to_html import markdown_to_html_node
from extract_title import extract_title


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


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from {from_path} "
        f"to {dest_path} using {template_path}"
    )

    # Ler o Markdown
    with open(from_path, "r") as f:
        markdown = f.read()

    # Ler o template
    with open(template_path, "r") as f:
        template = f.read()

    # Converter Markdown para HTML
    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()

    # Extrair o título
    title = extract_title(markdown)

    # Substituir os placeholders
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    # Criar diretórios necessários
    parent_dir = os.path.dirname(dest_path)

    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    # Escrever o HTML final
    with open(dest_path, "w") as f:
        f.write(template)


def main():
    print("Deleting public directory...")

    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_fyles_recursive(dir_path_static, dir_path_public)

    # Gerar a página principal
    generate_page(
        "content/index.md",
        "template.html",
        "public/index.html"
    )


if __name__ == "__main__":
    main()