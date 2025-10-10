import os
import shutil


def clear_destination(dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)
    print(f"fresh {dest_dir} has been created")


def copy_static(source_dir, dest_dir):
    if not os.path.exists(source_dir):
        raise Exception("source directory does not exist")

    source_items = os.listdir(source_dir)

    for item in source_items:
        item_path = os.path.join(source_dir, item)
        print(f"path for current source item {item_path}")
        if os.path.isfile(item_path):
            shutil.copy(item_path, dest_dir)
            print(f"source item {item} copied to destination {dest_dir}")

        else:
            print(f"{item} is a directory")
            new_dest = os.path.join(dest_dir, item)
            if not os.path.exists(new_dest):
                print(f"creating new directory in destination {new_dest}")
                os.mkdir(new_dest)
            copy_static(item_path, new_dest)
