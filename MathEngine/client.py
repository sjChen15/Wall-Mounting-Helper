import socket


def send_image(host, port, image_path):
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((host, port))
    print("Connected!")

    # Read the image data
    with open(image_path, "rb") as file:
        image_data = file.read()

    # Send the image data
    client_socket.sendall(image_data)
    print("Image sent!")

    # Close the socket
    client_socket.close()


# Usage
host = "10.0.0.86"  # Specify the server host
port = 9999  # Specify the server port
#image_path = "C:\\Users\\shiji\\OneDrive\\Documents\\Wall-Mounting-Helper\\MathEngine\\img.png"  # Specify the path to the image file
image_path = "C:\\Users\\shiji\\OneDrive\\Documents\\Wall-Mounting-Helper\\MathEngine\\SampleImage.png"
send_image(host, port, image_path)
