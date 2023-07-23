#image_receive_process.py

import socket
#import cv2
import numpy as np

port = 9999
# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific port
server_socket.bind(("0.0.0.0", port))


def receive_image(port, save_path):
    # Listen for incoming connections
    server_socket.listen(1)
    print("Waiting for connection...")

    # Accept a client connection
    client_socket, address = server_socket.accept()
    print("Connected!")

    # Receive the image data
    image_data = bytearray()
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        image_data += data

    # Save the image to a file
    with open(save_path, "wb") as file:
        file.write(image_data)
        print(f"Image saved to: {save_path}")
    client_socket.close()

img_num = 0
#new_image_ready = False
save_path = ""

#def new_image_ready():
#    if new_image_ready:
#        new_image_ready = False
#        return True
#    return False

#def get_recent_filename():
#    return save_path
    

while True:
    save_path = ("imgs/received_image_" + str(img_num) + ".jpg")  # Specify the path to save the received image
    receive_image(port, save_path)
    #new_image_ready = True
    img_num += 1
    if img_num >= 3:
        break
    
# Close the sockets
server_socket.close()
