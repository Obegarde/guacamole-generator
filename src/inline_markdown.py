from htmlnode import LeafNode
import re
from textnode import TextNode
from constants import *


#Converts a text node to a LeafNode
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case 'text':
            return LeafNode(None,text_node.text,None)
        case 'bold':
            return LeafNode("b",text_node.text,None)
        case 'italic':
            return LeafNode("i",text_node.text,None)
        case 'code':
            return LeafNode("code",text_node.text,None)
        case 'link':
            return LeafNode("a",text_node.text,{"href":text_node.url})
        case 'image':
            return LeafNode("img","",{"src":text_node.url,"alt":text_node.text})
        case _:
            raise Exception("Unsupported Text Type")
#Splits markdown and returns it as a TextNode
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    out_array = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            out_array.append(node)
            continue
        split_nodes = []
        temp_array = node.text.split(delimiter)
        if len(temp_array) % 2 == 0:
            raise ValueError("Invalid Markdown, formatted section not closed",temp_array)
        for i in range(len(temp_array)):
            if temp_array[i] == "":
                continue
            if i % 2  == 0:
                split_nodes.append(TextNode(temp_array[i],text_type_text))
            else:
                split_nodes.append(TextNode(temp_array[i], text_type))
        out_array.extend(split_nodes)
    return out_array

# Extracts images from markdown and returns a list of tuples (alt text, url)
def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text) 
    return matches
# Extracts links from markdown and returns a list of tuples(alt text, url)
def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)",text)
    return matches


#Splits nodes into either a link type TextNode or a text type TextNode
def split_nodes_link(old_nodes):
    out_array=[]
    for node in old_nodes:
        if node.text_type != text_type_text:
            out_array.append(node)
            continue
        split_nodes = []
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            out_array.append(node)
            continue
        text_section = node.text
        for match in  matches: 
            sections = text_section.split(f"[{match[0]}]({match[1]})", 1)
            
            if sections[0] != "": 
                split_nodes.append(TextNode(sections[0],text_type_text))

            split_nodes.append(TextNode(match[0],text_type_link,match[1]))
            text_section = sections[1]
        if text_section:
            split_nodes.append(TextNode(text_section,text_type_text))
        
        out_array.extend(split_nodes) 
    return out_array
        
#Splits nodes into either an image text type TextNode or a text type TextNode        
def split_nodes_image(old_nodes):
    out_array=[]
    for node in old_nodes:
        if node.text_type != text_type_text:
            out_array.append(node)
            continue
        split_nodes = []
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            out_array.append(node)
            continue
        text_section = node.text
        for match in  matches: 
            sections = text_section.split(f"![{match[0]}]({match[1]})", 1)
            
            if sections[0] != "": 
                split_nodes.append(TextNode(sections[0],text_type_text))

            split_nodes.append(TextNode(match[0],text_type_image,match[1]))
            text_section = sections[1]
        if text_section:
            split_nodes.append(TextNode(text_section,text_type_text))
        
        out_array.extend(split_nodes) 
    return out_array

#Combines all the previous functions and takes markdown and splits it into a list of TextNodes    
def text_to_textnodes(text):
    nodified_text = TextNode(text, text_type_text)
    return split_nodes_image(split_nodes_link(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter([nodified_text],'**',text_type_bold),'*',text_type_italic),'`',text_type_code)))
