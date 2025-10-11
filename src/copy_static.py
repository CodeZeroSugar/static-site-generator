import os
import shutil


def clear_destination(dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)


def copy_static(source_dir, dest_dir):
    if not os.path.exists(source_dir):
        raise Exception("source directory does not exist")

    source_items = os.listdir(source_dir)

    for item in source_items:
        item_path = os.path.join(source_dir, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, dest_dir)

        else:
            new_dest = os.path.join(dest_dir, item)
            if not os.path.exists(new_dest):
                os.mkdir(new_dest)
            copy_static(item_path, new_dest)
