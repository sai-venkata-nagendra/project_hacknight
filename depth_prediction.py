import numpy as np
import cv2
from keras.models import load_model
from keras.losses import MeanSquaredError
import os

# Load the trained depth estimation model
model_path = "output/depth_model.h5"

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Error: Model file '{model_path}' not found! Train the model first.")

# Load the model with custom loss function handling
model = load_model(model_path, custom_objects={"mse": MeanSquaredError()})

# Load input image for depth prediction
input_image_path = "input_blueprints/sample.jpg"  # Change this to the actual image file

if not os.path.exists(input_image_path):
    raise FileNotFoundError(f"Error: Input image '{input_image_path}' not found!")

img = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, (256, 256))  # Resize to match model input size
img = img / 255.0  # Normalize pixel values
img = np.expand_dims(img, axis=0)  # Add batch dimension
img = np.expand_dims(img, axis=-1)  # Add channel dimension

# Predict depth map
depth_map = model.predict(img)[0]  # Remove batch dimension

# Save the predicted depth map
output_depth_path = "output/depth_map.npy"
np.save(output_depth_path, depth_map)
print(f"Depth map saved at '{output_depth_path}'.")

# Optionally, visualize the depth map
depth_map_vis = (depth_map * 255).astype(np.uint8)  # Convert to grayscale image format
cv2.imwrite("output/depth_map.png", depth_map_vis)
print("Depth map image saved at 'output/depth_map.png'.")