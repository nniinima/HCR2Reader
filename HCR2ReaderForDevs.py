#This version is for developers who want touse the scripts for other purposes, it's a standalone script without GUI and thus easier to modify for your needs.

import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pytesseract
from skimage import io
from skimage.color import rgb2hsv
import pandas as pd

#This version of the script is run without the GUI and it takes inpput from a folder it is run in. Easier to modify for other purposes.

# Get the current directory
directory = os.getcwd()

# Get a list of PNG files in the directory
png_files = [filename for filename in os.listdir(directory) if filename.endswith(".png")]

# Initialize the array for storing the results
results = []

# Iterate over the PNG files in the directory
for png_file in png_files:
    print(f"Processing file {png_file}")
    # Read the original image
    img_rgb = io.imread(png_file)

    # Convert the image to a NumPy array
    data = np.array(img_rgb)

    # Crop another version of the image
    another_roi = Image.fromarray(img_rgb).crop((500, 400, 1000, Image.fromarray(img_rgb).height))
    another_img_to_plot = np.array(another_roi)

    # Apply color thresholding
    white_threshold = 255 - 10
    mask_white = (data > [white_threshold, white_threshold, white_threshold]).all(axis=-1)

    # Define the target color and tolerance
    target_color = np.array([235, 170, 8])  # ebaa08
    tolerance = 0.02  # 2% tolerance

    # Check if the color within the specified rectangle is within tolerance of the target color
    x_start, y_start = 500, 550
    x_end, y_end = 1350, 1250
    target_pixels = data[y_start:y_end, x_start:x_end]
    reshaped_target_color = np.tile(target_color, (target_pixels.shape[0], target_pixels.shape[1], 1))
    distances = np.linalg.norm(target_pixels - reshaped_target_color, axis=-1)
    mask_tolerance = np.zeros_like(mask_white)
    mask_tolerance[y_start:y_end, x_start:x_end] = distances / 255 <= tolerance

    # Combine the mask_tolerance with mask_white
    mask_white |= mask_tolerance

    # Apply the mask to convert matching colors to white
    data[mask_white] = [0, 0, 0]
    data[~mask_white] = [255, 255, 255]

    # Apply white rectangles and other preprocessing steps
    data[400:1400, 450:545] = data[:, :175] = data[:250, :] = [255, 255, 255]
    data[390:545, :] = [255, 255, 255]
    data[:, 1000:1150] = [255, 255, 255]
    data[440:, 1440:] = [255, 255, 255]

    # Convert back to image
    preprocessed_img = Image.fromarray(data)

    # Set tesseract path for Windows
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    # OCR on different regions of interest
    team1_roi = preprocessed_img.crop((0, 200, 1000, 400))
    team2_roi = preprocessed_img.crop((1000, 200, preprocessed_img.width, 400))
    score_roi = preprocessed_img.crop((100, 400, 300, preprocessed_img.height))
    player_roi = preprocessed_img.crop((500, 400, 1000, preprocessed_img.height))
    points_roi = preprocessed_img.crop((1180, 545, 1360, 1230))

    team1_text = pytesseract.image_to_string(team1_roi)
    team2_text = pytesseract.image_to_string(team2_roi)
    score_text = pytesseract.image_to_string(score_roi)
    player_text = pytesseract.image_to_string(player_roi)
    points_text = pytesseract.image_to_string(points_roi).replace(" ", "")

    # Format the OCR results by removing empty lines
    team1_text = '\n'.join(line for line in team1_text.splitlines() if line.strip())
    team2_text = '\n'.join(line for line in team2_text.splitlines() if line.strip())
    score_text = '\n'.join(line for line in score_text.splitlines() if line.strip())
    player_text = '\n'.join(line for line in player_text.splitlines() if line.strip())
    points_text = '\n'.join(line for line in points_text.splitlines() if line.strip())

    # Initialize a list to store the color objects
    colors = []

    # Obtain the OCR results and check the coordinates
    player_boxes = pytesseract.image_to_boxes(player_roi)
    image_height = player_roi.height

    # Initialize the previous y-coordinate
    prev_y2 = None

    for line in player_boxes.splitlines():
        char, x1, y1, x2, y2, _ = line.split()
        # Convert the coordinates to integers
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
        # Adjust the y-coordinates
        y1, y2 = image_height - y1, image_height - y2

        # Check if it's the first letter of the line or at least 40 pixels below the previous letter
        if prev_y2 is None or y1 - prev_y2 >= 40:
            # Check the color 300 pixels to the right of the first letter on each line
            search_x = x2 + 320
            search_y = (y1 + y2) // 2  # Use the vertical center of the letter
            search_color = another_roi.getpixel((search_x, search_y))

            # Convert the RGB color tuple to HSV color
            hsv_color = rgb2hsv(np.array(search_color) / 255.0)

            # Convert the hue value to the range of 0 to 360
            hue = hsv_color[0] * 360

            # Check if the hue value is within the blue range
            if (hue <= 300 and hue >= 180):
                color = 'blue'
            # Check if the hue value is within the yellow range
            elif (hue >= 10 and hue <= 90):
                color = 'yellow'
            else:
                color = 'unknown'

            # Add the color object to the colors list
            colors.append(color)

        # Update prev_y2 with the current letter's y-coordinate
        prev_y2 = search_y

    # Split the results by line and create an array of objects
    lines = max(len(score_text.splitlines()), len(points_text.splitlines()))
    for i in range(lines):
        score = score_text.splitlines()[i] if i < len(score_text.splitlines()) else ""
        position = 0  # Placeholder for now
        player = player_text.splitlines()[i] if i < len(player_text.splitlines()) else ""
        points = points_text.splitlines()[i] if i < len(points_text.splitlines()) else ""
        color = colors[i]
        result = {
            "score": score,
            "position": position,
            "player": player,
            "points": points,
            "color": color
        }
        results.append(result)
    print(f"Result for {png_file}: {result}")

def get_score_mapping():
    # Manually create a mapping from position to score
    mapping = {
        1: 300,
        2: 280,
        3: 262,
        4: 244,
        5: 228,
        6: 213,
        7: 198,
        8: 185,
        9: 173,
        10: 161,
        11: 150,
        12: 140,
        13: 131,
        14: 122,
        15: 114,
        16: 107,
        17: 99,
        18: 93,
        19: 87,
        20: 81,
        21: 75,
        22: 70,
        23: 66,
        24: 61,
        25: 57,
        26: 54,
        27: 50,
        28: 47,
        29: 44,
        30: 41,
        31: 38,
        32: 35,
        33: 33,
        34: 31,
        35: 29,
        36: 27,
        37: 25,
        38: 24,
        39: 22,
        40: 21,
        41: 19,
        42: 18,
        43: 17,
        44: 16,
        45: 15,
        46: 14,
        47: 13,
        48: 12,
        51: 10,
    }
    # Fill in the mapping for the ranges
    for i in range(49, 51):
        mapping[i] = 11
    for i in range(52, 54):
        mapping[i] = 9
    for i in range(54, 56):
        mapping[i] = 8
    for i in range(56, 58):
        mapping[i] = 7
    for i in range(58, 61):
        mapping[i] = 6
    for i in range(61, 64):
        mapping[i] = 5
    for i in range(64, 68):
        mapping[i] = 4
    for i in range(68, 74):
        mapping[i] = 3
    for i in range(74, 84):
        mapping[i] = 2
    for i in range(84, 101):
        mapping[i] = 1

    return mapping

score_mapping = get_score_mapping()

# Sort and assign positions
results.sort(key=lambda x: int(x["points"]), reverse=True)
for i, result in enumerate(results):
    position = i + 1
    result["position"] = position
    result["score"] = score_mapping.get(position, 0)  # Assign the score from the mapping

# Print the sorted array of objects
for result in results:
    print(result)

# Create a DataFrame from results
df = pd.DataFrame(results)

# Count the number of non-null entries in each column
num_colors = df['color'].count()
num_players = df['player'].count()
num_points = df['points'].count()

# Check if the counts are equal
if num_colors == num_players == num_points:
    print(f'Found {num_colors} records each for colors, players, and points. The number of records match.')
else:
    print(f'Warning: The number of records do not match. Found {num_colors} color records, {num_players} player records, and {num_points} points records. There has been an issue reading the data and the result may be off.')

# Export to CSV
df.to_csv("output.csv", index=False)

# Define the column order
column_order = ['player', 'position', 'points', 'score', 'color']

# Reorder the columns
df = df[column_order]

# Export to CSV
df.to_csv("output.csv", index=False)
