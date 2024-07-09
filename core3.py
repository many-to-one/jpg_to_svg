import numpy as np
from pixels2svg import pixels2svg
import os


# Convert the image to SVG
# def main():
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     print('path -----------', script_dir)
#     input_image_relative_path = '2.png'
#     input_image_path = os.path.join(script_dir, input_image_relative_path)
#     # output_svg_path = os.path.splitext(input_image_path)[0] + '.svg'
#     count = 0
#     for tolerance in (0, 64): #64, 128, 256, 512
#         # first iteration will take a long time because there are many colors
#         svg_img = pixels2svg(input_image_path,
#                                  color_tolerance=tolerance)
#         count += 1
#         output_svg_path = os.path.splitext(input_image_path)[0] + f'{count}.svg'
#         svg_img.save_to_path(output_svg_path)



# if __name__ == '__main__':
#     main()



def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print('path -----------', script_dir)
    input_image_relative_path = 'ws1.png'
    input_image_path = os.path.join(script_dir, input_image_relative_path)
    # output_svg_path = os.path.splitext(input_image_path)[0] + '.svg'

    svg_img = pixels2svg(
        input_image_path, 
        color_tolerance=254,
        remove_background=True
        )

    output_svg_path = os.path.splitext(input_image_path)[0] + f'1.svg'
    svg_img.save_to_path(output_svg_path)



if __name__ == '__main__':
    main()



# import os
# import cv2
# from pixels2svg import pixels2svg

# def preprocess_to_black_and_white(image_path):
#     """
#     Converts the input image to a black and white image.
#     """
#     # Read the image
#     image = cv2.imread(image_path)
    
#     if image is None:
#         print(f"Error: Could not load image {image_path}")
#         return None
    
#     # Convert to grayscale
#     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     # Apply a binary threshold to convert the grayscale image to black and white
#     _, bw_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY)
    
#     # Save the black and white image to a temporary path
#     temp_bw_path = os.path.splitext(image_path)[0] + '_bw.png'
#     cv2.imwrite(temp_bw_path, bw_image)
    
#     return temp_bw_path

# def main():
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     input_image_relative_path = '2.png'  # Change this to your image file name
#     input_image_path = os.path.join(script_dir, input_image_relative_path)
    
#     # Preprocess the image to black and white
#     bw_image_path = preprocess_to_black_and_white(input_image_path)

#     if bw_image_path:
#         # Convert the black and white image to SVG
#         svg_img = pixels2svg(bw_image_path, color_tolerance=0)

#         # Save the SVG file
#         output_svg_path = os.path.splitext(input_image_path)[0] + '_bw.svg'
#         svg_img.save_to_path(output_svg_path)
        
#         # Clean up the temporary file
#         os.remove(bw_image_path)

#         print(f'Conversion complete. SVG saved to {output_svg_path}')
#     else:
#         print('Image preprocessing failed.')

# if __name__ == '__main__':
#     main()



# import os
# import cv2
# from pixels2svg import pixels2svg

# def preprocess_to_black_and_white(image_path):
#     """
#     Converts the input image to a black and white image.
#     """
#     # Read the image
#     image = cv2.imread(image_path)
    
#     if image is None:
#         print(f"Error: Could not load image {image_path}")
#         return None
    
#      # Resize the image to scale up, if needed, to improve edge detection
#     scaled_image = cv2.resize(image, (0, 0), fx=3, fy=3, interpolation=cv2.INTER_LINEAR)

#     # Convert the image to grayscale
#     gray_image = cv2.cvtColor(scaled_image, cv2.COLOR_BGR2GRAY)

#     blur_kernel_size=(5, 5)

#     blurred_image = cv2.GaussianBlur(gray_image, blur_kernel_size, 0)

#     canny_threshold1 = 100
#     canny_threshold2 = 200

#     # Apply Canny edge detection to find outlines with adjustable thresholds
#     edges = cv2.Canny(blurred_image, canny_threshold1, canny_threshold2)

#     # Find contours (shapes) in the image using adjustable retrieval mode and contour approximation method
#     contour_mode=cv2.RETR_EXTERNAL
#     contour_method=cv2.CHAIN_APPROX_NONE
#     contours, _ = cv2.findContours(edges, contour_mode, contour_method)

#     # Draw contours on a blank image (black background)
#     contour_image = np.zeros_like(gray_image)
#     cv2.drawContours(contour_image, contours, -1, (255), thickness=cv2.FILLED)

#     # Invert the colors to get black fill inside contours and white outside
#     inverted_image = cv2.bitwise_not(contour_image)

#     # # Create a white background image
#     # contour_image = np.ones_like(gray_image) * 255

#     # # Draw contours on the white background image (black fill)
#     # cv2.drawContours(contour_image, contours, -1, (0), thickness=cv2.FILLED)

    
#     # Save the black and white image to a temporary path
#     temp_bw_path = os.path.splitext(image_path)[0] + '_bw.png'
#     cv2.imwrite(temp_bw_path, inverted_image)
    
#     return temp_bw_path

# def main():
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     input_image_relative_path = '2.png'  # Change this to your image file name
#     input_image_path = os.path.join(script_dir, input_image_relative_path)
    
#     # Preprocess the image to black and white
#     bw_image_path = preprocess_to_black_and_white(input_image_path)

#     if bw_image_path:
#         # Convert the black and white image to SVG
#         svg_img = pixels2svg(bw_image_path, color_tolerance=0)

#         # Save the SVG file
#         output_svg_path = os.path.splitext(input_image_path)[0] + '_bw.svg'
#         svg_img.save_to_path(output_svg_path)
        
#         # Clean up the temporary file
#         os.remove(bw_image_path)

#         print(f'Conversion complete. SVG saved to {output_svg_path}')
#     else:
#         print('Image preprocessing failed.')

# if __name__ == '__main__':
#     main()