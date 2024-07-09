# # importing pycairo
# import cairo
 
# # creating a SVG surface
# # here geek95 is file name & 700, 700 is dimension
# with cairo.SVGSurface("1a.svg", 700, 700) as surface:
 
#     # creating a cairo context object for SVG surface
#     # using Context method
#     context = cairo.Context(surface)
 
#     # setting color of the context
#     context.set_source_rgb(0.2, 0.23, 0.9)
#     # creating a rectangle
#     context.rectangle(10, 15, 90, 60)
 
#     # Fill the color inside the rectangle
#     context.fill()
 
#     # setting color of the context
#     context.set_source_rgb(0.9, 0.1, 0.1)
#     # creating a rectangle
#     context.rectangle(130, 15, 90, 60)
 
#     # Fill the color inside the rectangle
#     context.fill()
 
#     # setting color of the context
#     context.set_source_rgb(0.4, 0.9, 0.4)
#     # creating a rectangle
#     context.rectangle(250, 15, 90, 60)
 
#     # Fill the color inside the rectangle
#     context.fill()
 
#     # printing message when file is saved
#     print("File Saved")


import cv2
import numpy as np
import cairo

def convert_to_vector(input_image_path, output_image_path, scale_factor=1.0, epsilon_factor=0.01, canny_threshold1=50, canny_threshold2=150, blur_kernel_size=(3, 3), contour_mode=cv2.RETR_TREE, contour_method=cv2.CHAIN_APPROX_SIMPLE, stroke_width=1, fill_color=(0, 0, 0), use_bilateral_filter=True, sigma_color=100, sigma_space=100):
    # Read the input image
    image = cv2.imread(input_image_path)

    if image is None:
        print(f"Error: Could not load image {input_image_path}")
        return
    
    # Get image dimensions
    height, width, _ = image.shape

    # Resize the image to scale up, if needed, to improve edge detection
    scaled_image = cv2.resize(image, (0, 0), fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(scaled_image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur or Bilateral filter based on the parameter
    if use_bilateral_filter:
        blurred_image = cv2.bilateralFilter(gray_image, d=9, sigmaColor=sigma_color, sigmaSpace=sigma_space)
    else:
        blurred_image = cv2.GaussianBlur(gray_image, blur_kernel_size, 0)

    # Apply Canny edge detection to find outlines with adjustable thresholds
    edges = cv2.Canny(blurred_image, canny_threshold1, canny_threshold2)

    # Find contours (shapes) in the image using adjustable retrieval mode and contour approximation method
    contours, hierarchy = cv2.findContours(edges, contour_mode, contour_method)

    # Create a cairo surface to draw the SVG
    surface = cairo.SVGSurface(output_image_path, width, height)
    context = cairo.Context(surface)

    # Set stroke properties
    context.set_line_width(stroke_width)
    context.set_source_rgb(*fill_color)

    # Helper function to add contour to cairo context
    def add_contour_to_cairo(contour, fill):
        # Simplify the contour using Ramer-Douglas-Peucker algorithm if needed
        epsilon = epsilon_factor * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # Move to the first point in the contour
        context.move_to(approx[0][0][0] / scale_factor, approx[0][0][1] / scale_factor)
        
        # Draw lines for the rest of the points in the contour
        for point in approx:
            context.line_to(point[0][0] / scale_factor, point[0][1] / scale_factor)
        
        # Close the path
        context.close_path()
        
        if fill:
            context.fill_preserve()
        
        context.stroke()

    # Iterate through contours and add them to the cairo context with proper fill
    for i, contour in enumerate(contours):
        # Check if the contour is an external or internal contour
        if hierarchy[0][i][3] == -1:  # External contour
            add_contour_to_cairo(contour, True)
        else:  # Internal contour
            add_contour_to_cairo(contour, False)

    # Finish drawing and save the SVG file
    surface.finish()

# Sample input and output file paths
input_image_path = r'D:\ALEX\2023\08\jpg\vectors\ws1.png'
output_image_path = r'D:\ALEX\2023\08\jpg\vectors\results\1a.svg'

# Call the function to convert the image to vectors with the best parameters found
convert_to_vector(input_image_path, output_image_path, scale_factor=4.0, epsilon_factor=0.00001, canny_threshold1=50, canny_threshold2=150, blur_kernel_size=(3, 3), contour_mode=cv2.RETR_TREE, contour_method=cv2.CHAIN_APPROX_SIMPLE, stroke_width=1, fill_color=(0, 0, 0), use_bilateral_filter=True, sigma_color=120, sigma_space=120)
