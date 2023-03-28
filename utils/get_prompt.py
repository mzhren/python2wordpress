from PIL import Image
# [Image file formats - Pillow (PIL Fork) 9.4.0 documentation](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html)
# open also sets Image.text to a dictionary of the values of the tEXt, zTXt, and iTXt chunks of the PNG image. Individual compressed chunks are limited to a decompressed size of PngImagePlugin.MAX_TEXT_CHUNK, by default 1MB, to prevent decompression bombs. Additionally, the total size of all of the text chunks is limited to PngImagePlugin.MAX_TEXT_MEMORY, defaulting to 64MB.

def get_prompt(image):
    if not image.endswith('.png'):
        return ''
    img = Image.open(image)
    text_chunks = img.text
    text_chunks = dict(text_chunks)
    for key, value in text_chunks.items():
        if 'Negative prompt' in value:
            return value
    return ''

if __name__ == '__main__':
    # read prompt from image
    # prompt = read_image_text_chunks('watermark.png')
    prompt = get_prompt('hastags.png')
    print(prompt)