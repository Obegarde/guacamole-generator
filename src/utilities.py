from htmlnode import LeafNode
import re
from textnode import TextNode
from constants import *


class Convert: 
    def text_node_to_html_node(text_node):
        match text_node.text_type:
            case 'text':
                return LeafNode(None,text_node.text,None)
            case 'bold':
                return LeafNode("b",text_node.text,None)
            case 'italic':
                return LeafNode("i",text_node.text,None)
            case 'code':
                return LeafNode("code",text_node.text_node,None)
            case 'link':
                return LeafNode("a",text_node.text,{"href":text_node.url})
            case 'image':
                return LeafNode("img","",{"src":text_node.url,"alt":text_node.text})
            case _:
                raise Exception("Unsupported Text Type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    out_array = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            out_array.append(node)
            continue
        split_nodes = []
        temp_array = node.text.split(delimiter)
        if len(temp_array) % 2 == 0:
            raise ValueError("Invalid Markdown, formatted section not closed")
        for i in range(len(temp_array)):
            if temp_array[i] == "":
                continue
            if i % 2  == 0:
                split_nodes.append(TextNode(temp_array[i],text_type_text))
            else:
                split_nodes.append(TextNode(temp_array[i], text_type))
        out_array.extend(split_nodes)
    return out_array


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text) 
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)",text)
    return matches
