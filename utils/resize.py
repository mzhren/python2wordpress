import traceback
from PIL import Image
import argparse

MAX_WIDTH = 1800

def resize(inputFile):
    ratio = 1
    long_side = 0
    image = Image.open(inputFile).convert('RGBA')
    width = image.size[0]
    height = image.size[1]
    long_side = max(width, height)

    if long_side > MAX_WIDTH:
        ratio = MAX_WIDTH / long_side

    newWidth = int(round(width * ratio))
    newHeight = int(round(height * ratio))

    newImage = image.resize((newWidth, newHeight), Image.Resampling.LANCZOS)
    # newImage.format = 'webp'
    # newImage.save(outputFile)
    return newImage



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Resize image')
    parser.add_argument('-i','--input', help='input file',required=True)
    parser.add_argument('-o','--output', help='output file',required=True)
    args = parser.parse_args()
    inputFile = args.input
    outputFile = args.output
    try:
        resize(inputFile, outputFile)
    except Exception as e:
    	traceback.print_exc(e)