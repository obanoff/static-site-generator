from textnode import TextNode
from block import markdown_to_html_node
from htmlnode import HTMLNode
import os, shutil, re
from pathlib import Path


def handle_error(func, path, exc_info):
    print(f"Error removing {path}: {exc_info}")


def copy(source, target):
    if not os.path.exists(source):
        raise Exception("source path does not exist")

    if not os.path.exists(target):
        os.makedirs(target)

    entries = os.listdir(source)

    for entry in entries:
        full_source_path = os.path.join(source, entry)
        full_target_path = os.path.join(target, entry)

        if os.path.isdir(os.path.join(source, entry)):
            copy(full_source_path, full_target_path)

        if os.path.isfile(os.path.join(source, entry)):
            shutil.copy(full_source_path, full_target_path)


def extract_title(markdown):
    pattern = r"^(?<!#)# (?!#).+"

    match = re.search(pattern, markdown)
    if match:
        return match.group()
    else:
        raise Exception("file does not have h1 header")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as markdown_file:
        markdown_content = markdown_file.read()

    with open(template_path, "r") as template_file:
        template_content = template_file.read()

    title = extract_title(markdown_content)
    html = markdown_to_html_node(markdown_content).to_html()

    template_complete = template_content.replace("{{ Title }}", title).replace(
        "{{ Content }}", html
    )

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(dest_path)

    with open(dest_path, "w") as dest_file:
        dest_file.write(template_complete)


def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    for entry in os.listdir(dir_path_content):
        path = os.path.join(dir_path_content, entry)

        if os.path.isdir(path):
            generate_pages_recursively(
                path, template_path, os.path.join(dest_dir_path, entry)
            )

        if os.path.isfile(path):
            generate_page(
                path,
                template_path,
                os.path.join(dest_dir_path, f"{os.path.splitext(entry)[0]}.html"),
            )


def main():
    source, target = "./static", "./public"

    if os.path.exists(target):
        shutil.rmtree(target, onexc=handle_error)

    copy(source, target)

    generate_pages_recursively("./content", "template.html", "./public")


main()
