from copy_static import clear_destination, copy_static
from generate_pages_recursive import generate_pages_recursive
import pathlib


def main():
    root_dir = pathlib.Path(__file__).resolve().parent.parent
    source_dir = root_dir.joinpath("static")
    destination_dir = root_dir.joinpath("public")

    clear_destination(str(destination_dir))

    copy_static(str(source_dir), str(destination_dir))

    content_dir = root_dir.joinpath("content")
    template_path = root_dir.joinpath("template.html")

    generate_pages_recursive(str(content_dir), str(template_path), str(destination_dir))


main()
