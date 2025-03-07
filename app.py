from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
import open3d as o3d
import os

app = Flask(__name__)

# Load the model with custom objects
model = load_model("output/depth_model.h5", custom_objects={"mse": MeanSquaredError()})

# Define the depth_map_to_point_cloud function
def depth_map_to_point_cloud(depth_map, scale=1.0):
    rows, cols = depth_map.shape
    points = []

    for i in range(rows):
        for j in range(cols):
            z = depth_map[i, j] * scale  # Scale depth values
            x = j - cols / 2  # Center x-coordinate
            y = i - rows / 2  # Center y-coordinate
            points.append([x, y, z])

    return np.array(points)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict_3d", methods=["POST"])
def predict_3d():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Load and preprocess the image
        image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, (256, 256)) / 255.0
        image = np.expand_dims(image, axis=(0, -1))

        # Predict depth map
        depth_map = model.predict(image).squeeze()

        # Convert depth map to 3D point cloud
        point_cloud = depth_map_to_point_cloud(depth_map)

        # Create Open3D point cloud
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(point_cloud)

        # Compute normals for the point cloud
        pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

        # Create and save 3D mesh using Poisson surface reconstruction
        mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)

        # Save the 3D model
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, "output_3d_model.obj")
        o3d.io.write_triangle_mesh(output_path, mesh)

        return jsonify({"message": f"3D model saved as {output_path}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)