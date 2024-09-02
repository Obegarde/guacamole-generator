from os.path import isdir, isfile
from re import template
from textnode import TextNode
import os
import shutil
from markdown_html import markdown_to_html_node, extract_title


def main():
    copy_to_target(
        "/home/ducky39101/repos/guacamole-generator/static",
        "/home/ducky39101/repos/guacamole-generator/public",
    )
    generate_pages_recursive(
        "/home/ducky39101/repos/guacamole-generator/content",
        "/home/ducky39101/repos/guacamole-generator/template.html",
        "/home/ducky39101/repos/guacamole-generator/public",
    )


def copy_to_target(start, end):
    if os.path.exists(start):
        if os.path.exists(end):
            shutil.rmtree(end)
        os.mkdir(end)
        file_copier(start, end)
    else:
        raise FileNotFoundError("No start files found")


def file_copier(src, dst):
    for item in os.listdir(src):
        if os.path.isdir(os.path.join(src, item)):
            os.mkdir(f"{dst}/{item}")
            file_copier(f"{src}/{item}", f"{dst}/{item}")
        else:
            shutil.copy(os.path.join(src, item), dst)


def generate_page(from_path, template_path, dest_path):
    dest_path_without_ext = dest_path.split(".")
    print(
        f"Generating page from {from_path} to {dest_path_without_ext[0]}.html using {template_path}"
    )
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as t:
        template = t.read()

    nodefied_markdown = markdown_to_html_node(markdown)

    html_string = nodefied_markdown.to_html()
    title = extract_title(markdown)
    title_added = template.replace("{{ Title }}", title)
    content_added = title_added.replace("{{ Content }}", html_string)
    with open(f"{dest_path_without_ext[0]}.html", "w") as writer:
        writer.write(content_added)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        if os.path.isdir(os.path.join(dir_path_content, item)):
            os.mkdir(f"{dest_dir_path}/{item}")
            generate_pages_recursive(
                os.path.join(dir_path_content, item),
                template_path,
                os.path.join(dest_dir_path, item),
            )
        elif os.path.isfile(os.path.join(dir_path_content, item)):
            generate_page(
                f"{dir_path_content}/{item}", template_path, f"{dest_dir_path}/{item}"
            )


if __name__ == "__main__":
    main()
