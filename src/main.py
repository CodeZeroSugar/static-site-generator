from copy_static import clear_destination, copy_static
import os


def main():
    source_dir = os.path.expanduser(
        "~/workspace/github.com/CodeZeroSugar/static-site-generator/static/"
    )
    destination_dir = os.path.expanduser(
        "~/workspace/github.com/CodeZeroSugar/static-site-generator/public/"
    )

    clear_destination(destination_dir)

    copy_static(source_dir, destination_dir)


main()
