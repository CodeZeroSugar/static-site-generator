import os
from extract_title import extract_title
from markdown_to_html_node import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    if not os.path.exists(dest_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with (
        open(from_path, "r", encoding="utf-8") as md_file,
        open(template_path, "r", encoding="utf-8") as template_file,
        open(dest_path, "w", encoding="utf-8") as new_file,
    ):
        read_md = md_file.read()
        read_template = template_file.read()

        node = markdown_to_html_node(read_md)
        html_string = node.to_html()

        title = extract_title(read_md)

        replace_title = read_template.replace("{{ Title }}", title)
        replace_content = replace_title.replace("{{ Content }}", html_string)

        new_file.write(replace_content)
