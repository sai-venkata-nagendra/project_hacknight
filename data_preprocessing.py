import os
import cv2
import numpy as np

def load_images_from_folder(folder, img_size=(256, 256)):
    images = []
    
    if not os.path.exists(folder):
        raise ValueError(f"Error: Folder '{folder}' does not exist!")

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Skipping non-image file: {filename}")
            continue
        
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        
        if img is None:
            print(f"Warning: Unable to read {file_path}")
            continue
        
        img = cv2.resize(img, img_size)  # Resize to a fixed size
        img = img / 255.0  # Normalize pixel values to [0, 1]
        images.append(img)

    if len(images) == 0:
        raise ValueError(f"Error: No images loaded from '{folder}'! Check file formats and folder path.")

    return np.array(images)

# Create output folder if not exists
os.makedirs("preprocessed", exist_ok=True)

# Load dataset
X = load_images_from_folder("input_blueprints")  
y = load_images_from_folder("annotated_blueprints")  

# Save preprocessed data
np.save("preprocessed/X_train.npy", X)
np.save("preprocessed/y_train.npy", y)

print("✅ Preprocessed data saved successfully!")