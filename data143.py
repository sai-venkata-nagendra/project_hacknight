import cv2
import numpy as np
import os
import random

# Number of images to generate
num_images = 300  # Increased for better training

# Define folder paths
input_folder = "input_blueprints"
annotated_folder = "annotated_blueprints"

# Create folders (delete old images first)
if os.path.exists(input_folder):
    for file in os.listdir(input_folder):
        os.remove(os.path.join(input_folder, file))
else:
    os.makedirs(input_folder)

if os.path.exists(annotated_folder):
    for file in os.listdir(annotated_folder):
        os.remove(os.path.join(annotated_folder, file))
else:
    os.makedirs(annotated_folder)

def generate_synthetic_blueprint(index):
    """Generate a synthetic blueprint with random rooms, walls, doors, and windows."""
    img = np.ones((256, 256, 3), dtype=np.uint8) * 255  # White background

    num_rooms = random.randint(3, 6)  # Number of rooms per blueprint
    rooms = []

    for _ in range(num_rooms):
        x1, y1 = random.randint(10, 200), random.randint(10, 200)
        x2, y2 = x1 + random.randint(40, 80), y1 + random.randint(40, 80)
        color = [random.randint(50, 200) for _ in range(3)]  # Random pastel-like colors

        # Draw filled rectangles for rooms
        cv2.rectangle(img, (x1, y1), (x2, y2), color, -1)

        # Draw walls (thicker borders)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), 3)

        # Draw doors and windows
        door_width = 10
        window_width = 15
        if random.random() > 0.5:  # Draw a door
            door_x = random.randint(x1 + 10, x2 - 10)
            cv2.rectangle(img, (door_x, y2 - 5), (door_x + door_width, y2), (0, 0, 255), -1)
        if random.random() > 0.5:  # Draw a window
            window_x = random.randint(x1 + 10, x2 - 10)
            cv2.rectangle(img, (window_x, y1 + 5), (window_x + window_width, y1 + 20), (255, 0, 0), -1)

        rooms.append((x1, y1, x2, y2, color))

    return img, rooms

def generate_annotated_blueprint(index, rooms):
    """Generate annotated blueprint with bounding boxes around rooms."""
    img = np.ones((256, 256, 3), dtype=np.uint8) * 255  # White background

    for (x1, y1, x2, y2, color) in rooms:
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), 2)  # Draw bounding box

    return img

# Generate images
for i in range(num_images):
    blueprint, rooms = generate_synthetic_blueprint(i)
    annotated = generate_annotated_blueprint(i, rooms)

    cv2.imwrite(os.path.join(input_folder, f"blueprint_{i}.png"), blueprint)
    cv2.imwrite(os.path.join(annotated_folder, f"blueprint_{i}.png"), annotated)

    print(f"Generated {i+1}/{num_images} images...", end="\r")  # Show progress

print(f"\n✅ Successfully generated {num_images} synthetic blueprint images!")