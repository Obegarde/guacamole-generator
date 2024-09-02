from textnode import TextNode
import os
import shutil
from markdown_html import markdown_to_html_node, extract_title
def main():
   copy_to_target("./static","./public")
   generate_page("content/index.md","template.html","public/index.html") 
    




def copy_to_target(start,end):
    if os.path.exists(start):
        if os.path.exists(end):
            shutil.rmtree(end)
        os.mkdir(end)
        file_copier(start,end)
    else:
        raise FileNotFoundError("No start files found")

def file_copier(src,dst):
    for item in os.listdir(src):
        if os.path.isdir(os.path.join(src,item)): 
            os.mkdir(f"{dst}/{item}")
            file_copier(f"{src}/{item}",f"{dst}/{item}")
        else:
            shutil.copy(os.path.join(src,item), dst)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as t:
        template = t.read()

    nodefied_markdown = markdown_to_html_node(markdown)

    html_string = nodefied_markdown.to_html()
    title = extract_title(markdown)
    title_added = template.replace("{{ Title }}", title)
    content_added = title_added.replace("{{ Content }}", html_string)

    with open(dest_path, 'w') as writer:
        writer.write(content_added)

if __name__ == "__main__":
    main()
