import os

import torch
import numpy as np
import copy

from deodr import read_obj
from deodr import Scene3D, Camera
from deodr.triangulated_mesh import ColoredTriMesh as ColoredTriMesh

def get_camera(camera_center, width, height, focal=None):
    if focal is None:
        focal = 2 * width
    rot = np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]])
    trans = -rot.T.dot(camera_center)
    intrinsic = np.array(
        [[focal, 0, width / 2], [0, focal, height / 2], [0, 0, 1]]
    )
    extrinsic = np.column_stack((rot, trans))
    return Camera(
        extrinsic=extrinsic,
        intrinsic=intrinsic,
        width=width,
        height=height
    )
folder = os.path.dirname(__file__)
vertices = np.load(os.path.join(folder, "vertices.npz"))
original_faces = np.load(os.path.join(folder, "faces.npz"))

print("shape", vertices.shape, original_faces.shape)



trans = np.array([0., 0., 0.])
new_vertices = vertices + trans

default_color = np.array([1.0, 1.0, 1.0])
default_light = {
    "directional": -np.array([0.0, 0.0, 0.0]),
    "ambient": np.array([1.0]),
}

faces=original_faces[2850:2855,:]

height = width = 1326
light_directional = (copy.copy(default_light["directional"]))
light_ambient = (copy.copy(default_light["ambient"]))
vertices_color = (copy.copy(default_color))[None,:]
camera_center = np.array([0.0, 0.0, 5.0])

camera = get_camera(camera_center, width, height)

scene = Scene3D()        
scene.set_light(light_directional=light_directional, light_ambient=light_ambient)
background_color = np.array([0.0, 0.0, 0.0])
scene.set_background(np.tile(background_color[None, None, :], (height, width, 1)))

mesh = ColoredTriMesh(faces, nb_vertices=new_vertices.shape[0], nb_colors=3)
mesh.set_vertices(new_vertices)
mesh.set_vertices_colors(np.tile(vertices_color, [mesh.nb_vertices, 1]))

trimesh_mesh = mesh.to_trimesh()
trimesh_mesh.save(os.path.join(folder, "mesh.ply"))
scene.set_mesh(mesh)

img = scene.render(camera)
print(np.any(np.isnan(img.detach().numpy())))


img.retain_grad()
loss = torch.mean(img)
loss.backward(retain_graph=True)
print("nan counts = ", img[torch.isnan(img)].shape) # nan counts =  torch.Size([387])
print("trans grad", trans.grad) # trans grad tensor([nan, nan, nan])