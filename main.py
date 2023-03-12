import numpy as np
from stl import mesh
import qrcode


def create_box(x, y, size, height, z=0):
    # Create a cube with the specified size and height at x and y coordinates
    # Create 8 vertices
    vertices = np.array(
        [
            [x, y, z],
            [x + size, y, z],
            [x + size, y + size, z],
            [x, y + size, z],
            [x, y, height + z],
            [x + size, y, height + z],
            [x + size, y + size, height + z],
            [x, y + size, height + z],
        ]
    )

    # Create 12 faces
    faces = np.array(
        [
            [0, 3, 1],
            [1, 3, 2],
            [0, 4, 7],
            [0, 7, 3],
            [4, 5, 6],
            [4, 6, 7],
            [5, 1, 2],
            [5, 2, 6],
            [2, 3, 6],
            [3, 7, 6],
            [0, 1, 5],
            [0, 5, 4],
        ]
    )

    # Create the mesh
    qr_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            qr_mesh.vectors[i][j] = vertices[f[j], :]

    return qr_mesh


def create_mesh_fromQR(img, size, height, add_plate=False):
    # For each black pixel in the QR code, create a cube
    # with the specified size and height

    # Get the QR code image as a numpy array
    img = np.array(img)

    # Get the size of the QR code
    img_size = img.shape[0]

    # Create an empty list to store the meshes
    qr_meshes = []

    for x in range(img_size):
        for y in range(img_size):
            if img[x, y] == 0:
                # Create the cube
                qr_mesh = create_box(x * size, y * size, size, height)
                # Append it to the list of meshes
                qr_meshes.append(qr_mesh)

    # Combine the meshes into a final mesh
    qr_mesh = mesh.Mesh(np.concatenate([m.data for m in qr_meshes]))

    # Add a plate to the bottom of the QR code that is one pixel larger
    if add_plate:
        plate_mesh = create_box(
            -size, -size, img_size * size + 2 * size, height, z=-height
        )
        qr_mesh = mesh.Mesh(np.concatenate([qr_mesh.data, plate_mesh.data]))

    return qr_mesh


def main():
    data_in = input("Enter data to encode: ")

    add_plate = False
    plate = input("Add plate? (y/n): ")
    if plate == "y":
        add_plate = True
    else:
        add_plate = False

    print("Creating QR code...")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=0,
    )
    qr.add_data(data_in)
    qr.make(fit=True)
    print("QR code created")

    img = qr.make_image(fill_color="black", back_color="white")

    # Create the mesh
    print("Creating mesh...")
    qr_mesh = create_mesh_fromQR(img, 1, 1, add_plate=add_plate)
    # Save the mesh
    qr_mesh.save("qr_mesh.stl")
    print("Mesh saved")


if __name__ == "__main__":
    main()
