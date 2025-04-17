import cv2
import numpy as np
from skimage.feature import local_binary_pattern

def segment_linen_by_color(image, lower_color, upper_color):
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Create a binary mask using the color range
    mask = cv2.inRange(hsv, lower_color, upper_color)
    
    # Refine the mask using morphological operations (optional)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    return mask

def extract_texture_features(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply LBP (Local Binary Patterns) for texture analysis
    radius = 1  # Radius of LBP neighborhood
    n_points = 8 * radius  # Number of points around the circle
    lbp = local_binary_pattern(gray, n_points, radius, method='uniform')
    
    # Compute the histogram of LBP values
    lbp_hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, 11), range=(0, 10))
    lbp_hist = lbp_hist.astype('float')
    lbp_hist /= (lbp_hist.sum() + 1e-6)  # Normalize histogram
    
    return lbp_hist

def combine_color_and_texture(image, lower_color, upper_color):
    # Step 1: Color segmentation
    color_mask = segment_linen_by_color(image, lower_color, upper_color)
    
    # Step 2: Texture analysis (LBP)
    lbp_hist = extract_texture_features(image)
    
    # Step 3: Combine the two (color + texture)
    # Here you can choose to combine the results in various ways:
    # 1. Apply the color mask on the image to isolate linens
    color_segmented_image = cv2.bitwise_and(image, image, mask=color_mask)
    
    # 2. Use texture features to identify linens based on fabric texture
    # You could use LBP histograms for further classification or refinement
    
    return color_segmented_image, lbp_hist

# Example usage
if __name__ == "__main__":
    # Load image
    image = cv2.imread("sheets.jpg")
    
    # Define color range for linens (off-white color range in HSV)
    lower_color = np.array([0, 0, 180])  # Lower bound
    upper_color = np.array([180, 60, 255])  # Upper bound
    
    # Combine color segmentation and texture extraction
    segmented_image, lbp_features = combine_color_and_texture(image, lower_color, upper_color)
    
    # Show the results
    cv2.imshow("Segmented Linens by Color", segmented_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

