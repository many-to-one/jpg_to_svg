# from PIL import Image
# import os

# def remove_transparency(im, bg_color=(255, 255, 255)):
#     if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
#         alpha = im.convert('RGBA').split()[-1]

#         bg = Image.new("RGBA", im.size, bg_color + (255,))
#         bg.paste(im, mask=alpha)
#         return bg
#     else:
#         return im


# def convert(input_image_path, output_image_path):
#     """
#     Converts the .png file to .eps file
#     """
#     im = Image.open(input_image_path)
#     if im.mode in ('RGBA', 'LA'):
#         im = remove_transparency(im)
#         im = im.convert('RGB')
#     im.save(output_image_path, lossless=True)


# def main():
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     input_image_relative_path = 'ws2.png'  # Change this to your image file name
#     output_image_relative_path = '1.eps'  # Change this to your desired output file name
#     input_image_path = os.path.join(script_dir, input_image_relative_path)
#     output_image_path = os.path.join(script_dir, output_image_relative_path)
    
#     convert(input_image_path, output_image_path)
#     print("Conversion finished. \nOutput path is {}".format(output_image_path))


# if __name__ == "__main__":
#     main()

from PIL import Image
import os

def convert(input_image_path, output_image_path):
    """
    Converts the .png file to .eps file without adding a background.
    """
    im = Image.open(input_image_path)
    if im.mode in ('RGBA', 'LA'):
        im = im.convert('RGB')  # Convert to RGB to ensure compatibility with EPS format
    im.save(output_image_path, lossless=True)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_image_relative_path = 'ws2.png'  # Change this to your image file name
    output_image_relative_path = '1.eps'  # Change this to your desired output file name
    input_image_path = os.path.join(script_dir, input_image_relative_path)
    output_image_path = os.path.join(script_dir, output_image_relative_path)
    
    convert(input_image_path, output_image_path)
    print("Conversion finished. \nOutput path is {}".format(output_image_path))


if __name__ == "__main__":
    main()

