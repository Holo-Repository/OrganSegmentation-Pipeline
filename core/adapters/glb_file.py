"""
This module contains functionality related to writing a mesh to disk as an GLB file.
"""
import logging
import numpy as np
import trimesh
from trimesh import repair
import trimesh.creation
from trimesh.smoothing import filter_laplacian,filter_taubin

def write_mesh_as_glb_with_colour(
    meshes, output_glb_file_path: str, iterations, colour=[], metadata={}
) -> None:
    scene = trimesh.Scene(metadata=metadata)
    index = 0
    if len(colour) != len(meshes):
        colour = get_random_rgb_colours(len(meshes))
    for mesh_data in meshes:
        mesh = trimesh.Trimesh(
            vertices=mesh_data[0], faces=mesh_data[1], vertex_normals=mesh_data[2]
        )
        filter_laplacian(mesh, iterations=iterations, volume_constraint=False)
        repair.fix_inversion(mesh)
        mesh.visual.material = trimesh.visual.material.SimpleMaterial(
            diffuse=np.asarray(colour[index])
        )
        scene.add_geometry(mesh)
        index += 1

    # Calculate the center of all the meshes in the scene
    center = np.mean(np.concatenate([mesh_data[0] for mesh_data in meshes]), axis=0)

    # Translate the scene so that its pivot aligns with the center of all the meshes
    for mesh in scene.geometry.items():
        mesh[1].vertices -= center

    scene.export(output_glb_file_path)

def get_random_rgb_colours(length, alpha=0.5):
    colour = np.random.rand(length, 3)
    alpha = np.ones((length, 1)) * alpha
    colour = (np.concatenate([colour, alpha], axis=1) * 255).astype(np.uint8)
    return colour
