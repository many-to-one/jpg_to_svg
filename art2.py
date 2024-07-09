import cv2
import numpy as np
import svgwrite

def convert_to_vector(input_image_path, 
                      output_image_path, 
                      scale_factor, 
                      epsilon_factor, 
                      canny_threshold1, 
                      canny_threshold2, 
                      blur_kernel_size, 
                      contour_mode=cv2.RETR_TREE, 
                      contour_method=cv2.CHAIN_APPROX_SIMPLE, 
                      stroke_width=1, fill_color='black', 
                      use_bilateral_filter=True, 
                      sigma_color=100, 
                      sigma_space=100):
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

    # Create an SVG drawing object with the same size as the original image
    dwg = svgwrite.Drawing(output_image_path, size=(width, height), profile='tiny')

    def add_contour_to_svg(contour, fill):
        # Simplify the contour using Ramer-Douglas-Peucker algorithm if needed
        if contour_method == cv2.CHAIN_APPROX_SIMPLE:
            epsilon = epsilon_factor * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            points = [(float(point[0][0]) / scale_factor, float(point[0][1]) / scale_factor) for point in approx]
        else:
            points = [(float(point[0][0]) / scale_factor, float(point[0][1]) / scale_factor) for point in contour]
        
        # Add a polygon to the SVG drawing
        dwg.add(dwg.polygon(points, stroke='black', fill=fill, stroke_width=stroke_width))

    # Iterate through contours and add them to the SVG drawing with proper fill
    for i, contour in enumerate(contours):
        # Check if the contour is an external or internal contour
        if hierarchy[0][i][3] == -1:  # External contour
            add_contour_to_svg(contour, fill_color)
        else:  # Internal contour
            add_contour_to_svg(contour, 'none')  # Do not fill internal contours
            print('---------- no fill -------------')

    # Save the SVG file
    dwg.save()

# Sample input and output file paths
input_image_path = r'D:\ALEX\2023\08\jpg\vectors\ws2.JPG'
output_image_path = r'D:\ALEX\2023\08\jpg\vectors\results\1a.svg'

# Call the function to convert the image to vectors with the best parameters found
convert_to_vector(input_image_path, output_image_path, scale_factor=4.0, epsilon_factor=0.0001, canny_threshold1=50, canny_threshold2=50, blur_kernel_size=(3, 3), contour_mode=cv2.RETR_TREE, contour_method=cv2.CHAIN_APPROX_SIMPLE, stroke_width=6, fill_color='black', use_bilateral_filter=True, sigma_color=120, sigma_space=120)
