import cv2
import numpy as np

def process_coins(image_path):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Preprocess the image (apply GaussianBlur and Canny Edge Detection)
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    edges = cv2.Canny(blurred, 30, 150)

    # Detect circles using Hough Circle Transform
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30, param1=50, param2=30, minRadius=15, maxRadius=50)

    # Prepare a blank image to visualize detection
    output_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # Initialize coin value counters
    coin_counts = {'10': 0, '25': 0, '1': 0}  # Values are in centavos (10c, 25c, 1 peso)
    total_value = 0

    # Process detected circles
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            # Draw the circle on the output image
            cv2.circle(output_image, (x, y), r, (0, 255, 0), 2)
            cv2.rectangle(output_image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

            # Classify coins based on their radius
            if r < 20:  # Example threshold for 10 centavos
                coin_counts['10'] += 1
                total_value += 10
            elif 20 <= r < 30:  # Example threshold for 25 centavos
                coin_counts['25'] += 1
                total_value += 25
            elif r >= 30:  # Example threshold for 1 peso
                coin_counts['1'] += 1
                total_value += 100  # 1 peso = 100 centavos

    # Save the output visualization
    output_path = r"C:\Users\Apeke\Downloads\coin_detection_output.jpeg"
    cv2.imwrite(output_path, output_image)

    return coin_counts, total_value, output_path

# Example usage
image_path = r"C:\Users\Apeke\Downloads\GetImage.jpeg"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
if image is None:
    raise FileNotFoundError(f"Image file not found or unable to load: {image_path}")

coin_counts, total_value, output_path = process_coins(image_path)

# Print results
print("Coin Counts:", coin_counts)
print("Total Value (centavos):", total_value)
print("Visualization saved at:", output_path)
