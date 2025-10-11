import os

from generate_page import generate_page


def generate_pages_recursive(
    dir_path_content, template_path, dest_dir_path, basepath=None
):
    dir_list = os.listdir(dir_path_content)

    for item in dir_list:
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path) and "index.md" == item:
            new_dest_path = os.path.join(dest_dir_path, "index.html")
            generate_page(item_path, template_path, new_dest_path, basepath)

        elif not os.path.isfile(item_path):
            new_dest_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(item_path, template_path, new_dest_path, basepath)

        else:
            continue
