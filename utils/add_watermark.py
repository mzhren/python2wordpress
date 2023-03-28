from PIL import Image,ImageEnhance

WATERMARK =  'watermark.png'
OPACITY = 0.6

def add_watermark(image,position_label='bottom-center'):
    """
    Add watermark to an image
    """
    layer = Image.new('RGBA', image.size, (0,0,0,0))

    watermark_image = Image.open(WATERMARK).convert('RGBA')

    r,g,b,a = watermark_image.split()
    # opacity为透明度，范围(0,1)
    alpha = ImageEnhance.Brightness(a).enhance(OPACITY)
    watermark_image.putalpha(alpha)

    layer = Image.alpha_composite(layer,image)
    position = set_position(image, watermark_image, position_label)
    layer.alpha_composite(watermark_image, position)
    return layer

def set_position(image, watermark_image, position,pad = 50):
    """
    Set position of watermark
    """
    if position == 'bottom-center':
        return ((int(image.width / 2 - watermark_image.width / 2)), (int(image.height - watermark_image.height - pad)))
    elif position == 'top-left':
        return (0, 0)
    elif position == 'top-right':
        return (image.width - watermark_image.width, 0)
    elif position == 'bottom-left':
        return (0, image.height - watermark_image.height)
    elif position == 'bottom-right':
        return (image.width - watermark_image.width, image.height - watermark_image.height)
    else:
        raise ValueError('Unknown position')
    

if __name__ == '__main__':
    image = Image.open('has_prompt_test.png').convert('RGBA')
    result = add_watermark(image)
    result.save('result.webp', 'webp', quality=80)