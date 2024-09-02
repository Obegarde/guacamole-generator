from block_markdown import markdown_to_blocks, block_to_block_type
from inline_markdown import text_node_to_html_node, text_to_textnodes
from htmlnode import HTMLNode,LeafNode,ParentNode
import re
from constants import (
    block_type_paragraph,
    block_type_olist,
    block_type_code,
    block_type_heading,
    block_type_quote,
    block_type_ulist,
    text_type_bold,
)

#Takes markdown and returns a single HTMLNode with all the included markdown as children
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    htmlnode_array = []
    for block in blocks:
       html_node = block_to_html_node(block)
       htmlnode_array.append(html_node)
         
    return ParentNode("div",htmlnode_array, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_olist:
        return olist_to_html_node(block)
    if block_type == block_type_ulist:
        return ulist_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")


def text_to_children(markdown):
    textnode_array = text_to_textnodes(markdown)
    out_array = []
    for node in textnode_array:
        out_array.append(text_node_to_html_node(node))
    return out_array



def heading_type(block):
    if re.match(r"^#{6}", block):
        return 'h6'
    elif re.match(r"^#{5}", block):
        return 'h5'
    elif re.match(r"^#{4}", block):
        return 'h4'
    elif re.match(r"^#{3}", block):
        return 'h3'
    elif re.match(r"^#{2}", block):
        return 'h2'
    elif re.match(r"^#{1}", block):
        return 'h1'



def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre",[code])

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li",children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines: 
        title = re.match(r"#\s.+",line)
        if title != None: 
            return title.group().replace("#","").strip()
    
    raise Exception("No Title Found")
