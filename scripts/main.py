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
    mask = np.where(mask > 0, 255, 0).astype(np.uint8)
    
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


def overlay_section_info(image, sections_with_types, grid=(4, 4)):
    """
    Overlay the section information (linen type and percentage of white) and grid divisions onto the image.
    
    Parameters:
        image (np.ndarray): The skewed/cropped image.
        sections_with_types (list): Sections with percentage and linen type.
        grid (tuple): Grid dimensions (rows, cols) for sectioning.
        
    Returns:
        image_with_overlay (np.ndarray): The image with section info and grid overlayed.
    """
    height, width = image.shape[:2]
    rows, cols = grid
    section_height = height // rows
    section_width = width // cols

    image_with_overlay = image.copy()

    # Loop through each section and overlay text
    for section in sections_with_types:
        row, col = section['row'], section['col']
        y1, y2 = row * section_height, (row + 1) * section_height
        x1, x2 = col * section_width, (col + 1) * section_width

        # Draw the grid line (rectangle)
        cv2.rectangle(image_with_overlay, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Text to overlay (linen type and white ratio percentage)
        text = f"{section['linen_type']} ({section['white_ratio']*100:.1f}%)"
        position = (x1 + 5, y1 + 15)

        # Put text on the image (linen type and white percentage)
        cv2.putText(image_with_overlay, text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.2, (255, 255, 255), 1, cv2.LINE_AA)

    # Overlay grid divisions (lines between sections)
    for row in range(1, rows):
        y = row * section_height
        cv2.line(image_with_overlay, (0, y), (width, y), (255, 0, 0), 2)  # Horizontal lines

    for col in range(1, cols):
        x = col * section_width
        cv2.line(image_with_overlay, (x, 0), (x, height), (255, 0, 0), 2)  # Vertical lines

    return image_with_overlay

def assign_linen_types(sections, linen_types):
    """
    Assigns linen types to sections based on a predefined list of linen types.
    
    Parameters:
        sections (list of dicts): The section data with white pixel ratios.
        linen_types (list): List of linen types in order, should match the grid's size.
        
    Returns:
        sections_with_types (list): Updated section data with linen types assigned.
    """
    if len(sections) != len(linen_types):
        raise ValueError("Number of linen types must match the number of sections.")
    
    for i, section in enumerate(sections):
        section['linen_type'] = linen_types[i]

    return sections

def analyze_sections(image, grid=(4, 4), white_threshold=200):
    """
    Divides an image into a grid and calculates the percentage of white pixels per section.
    
    Parameters:
        image (np.ndarray): The skewed/cropped image.
        grid (tuple): Number of (rows, cols) to split the image into.
        white_threshold (int): Pixel intensity threshold to consider as "white".
        
    Returns:
        section_data (list of dicts): Each dict has position, white pixel ratio, and linen type.
    """
    height, width = image.shape[:2]
    rows, cols = grid
    section_height = height // rows
    section_width = width // cols

    section_data = []

    # Define color range for linens (off-white color range in HSV)
    lower_color = np.array([0, 0, 180])  # Lower bound
    upper_color = np.array([180, 60, 255])  # Upper bound

    # Convert to grayscale
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    segmented_image, lbp_features = combine_color_and_texture(image, lower_color, upper_color)
    segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Image with Section Info", segmented_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    for row in range(rows):
        for col in range(cols):
            y1 = row * section_height
            y2 = (row + 1) * section_height
            x1 = col * section_width
            x2 = (col + 1) * section_width

            section = segmented_image[y1:y2, x1:x2]
            total_pixels = section.size
            white_pixels = cv2.countNonZero(cv2.threshold(section, white_threshold, 255, cv2.THRESH_BINARY)[1])
            white_ratio = white_pixels / total_pixels

            section_data.append({
                'row': row,
                'col': col,
                'white_ratio': white_ratio,
                'status': 'full' if white_ratio > 0.8 else 'partial' if white_ratio > 0.2 else 'empty'
            })

    return section_data

def crop_and_skew(image_path, coords, output_size=(500, 500)):
    """
    Crops and applies a perspective transform to the specified region of an image.
    
    Parameters:
        image_path (str): Path to the input image.
        coords (list): List of four (x, y) tuples for the corners in the order:
                       top-left, top-right, bottom-right, bottom-left.
        output_size (tuple): Size of the output image (width, height).
        
    Returns:
        warped (np.ndarray): The transformed (cropped + skewed) image.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or invalid path")

    pts_src = np.array(coords, dtype="float32")
    width, height = output_size

    # Define destination points to map to
    pts_dst = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype="float32")

    # Compute the perspective transform matrix
    M = cv2.getPerspectiveTransform(pts_src, pts_dst)
    warped = cv2.warpPerspective(image, M, (width, height))

    return warped

# Example usage
if __name__ == "__main__":
    coords = [(316, 494), (999, 526), (945, 1505), (315, 1512)]  # Sample coordinates
    skewed_image = crop_and_skew("sheets.jpg", coords)

    cv2.imshow("Cropped and Skewed", skewed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
	# Analyze sections
    sections = analyze_sections(skewed_image, grid=(10, 10))
    
    # Define linen types for each section (manual assignment based on your image layout)
    linen_types = [
		'King', 'Single', 'Towel', 'FaceTowel', 'King', 'Single', 'Towel', 'FaceTowel', 
		'King', 'Single', 'Towel', 'FaceTowel', 'King', 'Single', 'Towel', 'FaceTowel',
		'King', 'Single', 'Towel', 'FaceTowel', 'King', 'Single', 'Towel', 'FaceTowel',
		'King', 'Single', 'Towel', 'FaceTowel', 'King', 'Single', 'Towel', 'FaceTowel',
		'King', 'Single', 'Towel', 'FaceTowel', 'King', 'Single', 'Towel', 'FaceTowel',
		'King', 'Single', 'Towel', 'FaceTowel', 'King', 'Single', 'Towel', 'FaceTowel',
		'King', 'Single', 'Towel', 'FaceTowel', 'King', 'Single', 'Towel', 'FaceTowel',
		'King', 'Single', 'Towel', 'FaceTowel', 'King', 'Single', 'Towel', 'FaceTowel',
		'King', 'Single', 'Towel', 'FaceTowel', 'King', 'Single', 'Towel', 'FaceTowel',
		'King', 'Single', 'Towel', 'FaceTowel', 'King', 'Single', 'Towel', 'FaceTowel'
	]
    linen_types_grid = [[None for _ in range(10)] for _ in range(10)]
    linen_types = [item for row in linen_types_grid for item in row]

    # Assign linen types to sections
    sections_with_types = assign_linen_types(sections, linen_types)

    # Print out section data
    for s in sections_with_types:
        print(f"Section ({s['row']}, {s['col']}): {s['white_ratio']*100:.1f}% white → {s['status']} → Linen Type: {s['linen_type']}")

    # Overlay the section info and grid divisions onto the image
    image_with_overlay = overlay_section_info(skewed_image, sections_with_types,grid=(10,10))

    # Show the image with overlays
    cv2.imshow("Image with Section Info", image_with_overlay)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
