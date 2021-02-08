import PIL
from PIL import Image
import os

def image_compressor():
    width = 672
    height = 936

    os.chdir('images/')

    images = os.listdir()

    for image in images:
        img = Image.open(image)
        img = img.resize((height, width), PIL.Image.ANTIALIAS)
        img.save(image, optimize=True,quality=30)
        print('Compressing '+image + '...')

    os.chdir('..')
if __name__ == '__main__':
    width = 672
    height = 936

    os.chdir('images/')

    images = os.listdir()
    err = []
    for image in images:
        try:
            img = Image.open(image)
            img = img.resize((height, width), PIL.Image.ANTIALIAS)
            img.save(image, optimize=True,quality=50)
        except:
            err.append(image)
        print('Compressing '+image + '...')
    print('Image files with Errors: '+ str(err))
    os.chdir('..')
