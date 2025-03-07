import os
import numpy as np
import open3d as o3d

# Load the depth map
depth_map = np.load("output/depth_map.npy")
depth_map = depth_map.squeeze()  # Remove extra dimensions

# Generate 3D point cloud from depth map
height, width = depth_map.shape
x, y = np.meshgrid(np.linspace(-1, 1, width), np.linspace(-1, 1, height))
z = depth_map.flatten()
points = np.vstack((x.flatten(), y.flatten(), z)).T

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)

# Compute normals for the point cloud
pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
pcd.orient_normals_consistent_tangent_plane(100)

# Poisson surface reconstruction
mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)

# Save 3D mesh
os.makedirs("output", exist_ok=True)
o3d.io.write_triangle_mesh("output/3d_mesh.obj", mesh)

print("✅ 3D mesh saved successfully at 'output/3d_mesh.obj'")