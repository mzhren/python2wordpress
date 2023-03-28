import os
import argparse
from webp import images_handler


def get_folders(input_folder):
    folders = [f for f in os.listdir(
        input_folder) if os.path.isdir(os.path.join(input_folder, f))]
    folders = [f for f in folders if not os.path.isdir(os.path.join(input_folder, f, 'output'))]
    return folders

def main():
    args = get_args()
    input_folder = args.folder
    folders = get_folders(input_folder)
    for folder in folders:
        print('doing', folder)
        output_folder = os.path.join(input_folder, folder, 'output')
        if not os.path.isdir(output_folder):
            os.mkdir(output_folder)
        images_handler(os.path.join(input_folder, folder), os.path.join(input_folder, folder, 'output'))
        print('done', folder)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', help='Choose Folder', required=True)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()