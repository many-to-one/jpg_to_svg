import cv2
import numpy as np
import svgwrite
import random

def convert_to_vector(input_image_path, output_image_path, scale_factor=1.0, epsilon_factor=0.01, canny_threshold1=100, canny_threshold2=200, blur_kernel_size=(5, 5), contour_mode=cv2.RETR_EXTERNAL, contour_method=cv2.CHAIN_APPROX_NONE, stroke_width=1, fill_color='black', use_bilateral_filter=False, max_random_offset=10):
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

    # Apply Gaussian blur or bilateral filter to smooth the image
    if use_bilateral_filter:
        blurred_image = cv2.bilateralFilter(gray_image, d=9, sigmaColor=75, sigmaSpace=75)
    else:
        blurred_image = cv2.GaussianBlur(gray_image, blur_kernel_size, 0)

    # Apply Canny edge detection to find outlines with adjustable thresholds
    edges = cv2.Canny(blurred_image, canny_threshold1, canny_threshold2)

    # Find contours (shapes) in the image using adjustable retrieval mode and contour approximation method
    contours, _ = cv2.findContours(edges, contour_mode, contour_method)

    # Create an SVG drawing object with the same size as the original image
    dwg = svgwrite.Drawing(output_image_path, size=(width, height), profile='tiny')

    # Iterate through contours and add them to the SVG drawing
    for contour in contours:
        # Randomize the position by adding a random offset
        x_offset = random.randint(-max_random_offset, max_random_offset)
        y_offset = random.randint(-max_random_offset, max_random_offset)

        if contour_method == cv2.CHAIN_APPROX_SIMPLE:
            # Simplify the contour using Ramer-Douglas-Peucker algorithm (optional)
            epsilon = epsilon_factor * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            points = [(float(point[0][0]) / scale_factor + x_offset, float(point[0][1]) / scale_factor + y_offset) for point in approx]
        else:
            # Use all points in the contour (higher detail)
            points = [(float(point[0][0]) / scale_factor + x_offset, float(point[0][1]) / scale_factor + y_offset) for point in contour]

        # Ensure the points stay within the bounds of the image
        points = [(min(max(0, x), width), min(max(0, y), height)) for x, y in points]

        # Add a polygon to the SVG drawing with a fill
        dwg.add(dwg.polygon(points, stroke='black', fill=fill_color, stroke_width=stroke_width))

    # Save the SVG file
    dwg.save()

# Sample input and output file paths
input_image_path = r'D:\ALEX\2023\08\jpg\vectors\2.JPG'
output_image_path = r'D:\ALEX\2023\08\jpg\vectors\results\1.svg'

# Call the function to convert the image to vectors with adjustable parameters
convert_to_vector(input_image_path, output_image_path, scale_factor=2.0, epsilon_factor=0.00001, canny_threshold1=50, canny_threshold2=150, blur_kernel_size=(3, 3), contour_mode=cv2.RETR_TREE, contour_method=cv2.CHAIN_APPROX_NONE, stroke_width=1.5, fill_color='black', use_bilateral_filter=True, max_random_offset=50)
