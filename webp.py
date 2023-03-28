from utils.resize import resize
from utils.add_watermark import add_watermark
from utils.get_prompt import get_prompt
import argparse
import glob
import os


def resize_and_addwatermark(inputFile, outputFile):
    image = resize(inputFile)
    result = add_watermark(image)
    result.save(outputFile, 'webp', quality=80)


def images_handler(inputFolder, outputFolder, image_name='girl'):
   # get png/jpg files and index them
    images = glob.glob(inputFolder + "/*.png")
    images.extend(glob.glob(inputFolder + "/*.jpg"))
    images.extend(glob.glob(inputFolder + "/*.jpeg"))

    name_index = 0
    has_prompt = False

    for image in images:
        if os.path.isfile(image):
            has_prompt = generate_prompt(image, has_prompt, outputFolder)
            print('doing', image)
            file_name = image_name + str(name_index) + ".webp"
            name_index += 1
            output_file = os.path.join(outputFolder, file_name)
            resize_and_addwatermark(image, output_file)
            print('done', image, 'to', output_file)
    print('done all')


def generate_prompt(image, has_prompt, outputFolder):
    if not has_prompt:
        prompt = get_prompt(image)
        if prompt:
            has_prompt = True
            prompt_file = os.path.join(outputFolder, 'prompt.txt')
            with open(prompt_file, 'w', encoding='utf8') as f:
                f.write(prompt)
                print('done', prompt_file)
    return has_prompt


def get_args():
    parser = argparse.ArgumentParser(
        description='Resize image and add watermark')
    parser.add_argument('-i', '--input', help='input folder', required=True)
    parser.add_argument('-n', '--name', help='name of images', default='girl_')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    inputFolder = args.input
    outputFolder = inputFolder + "\output"
    name = args.name
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    images_handler(inputFolder, outputFolder, name)
