import socket
import cv2
import numpy as np


def receive_image(port, save_path):
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific port
    server_socket.bind(("localhost", port))

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

    # Close the sockets
    client_socket.close()
    server_socket.close()


def mask_green_ref_img(image_path):
    image_data = cv2.imread(image_path)

    # It converts the BGR color space of image to HSV color space
    hsv = cv2.cvtColor(image_data, cv2.COLOR_BGR2HSV)

    # Threshold of blue in HSV space
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([70, 255, 255])

    # preparing the mask to overlay
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # The black region in the mask has the value of 0,
    # so when multiplied with original image removes all non-blue regions
    result = cv2.bitwise_and(image_data, image_data, mask=mask)

    cv2.imshow("img", image_data)
    cv2.imshow("mask", mask)

    cv2.imshow("result", result)

    grayscale_result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    cv2.imshow("gray_result", grayscale_result)

    cv2.waitKey(0)

    return image_data, grayscale_result


def harris_corners(img, mask):
    # take the grayscale mask and apply the harris corners to it

    gray = np.float32(mask)
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)
    cv2.imshow("test", dst)
    # result is dilated for marking the corners, not important
    dst = cv2.dilate(dst, None)

    print(dst > 0.01 * dst.max())

    # Threshold for an optimal value, it may vary depending on the image.
    img[dst > 0.01 * dst.max()] = [0, 0, 255]

    cv2.imshow("mask", mask)
    cv2.imshow("dst", img)
    cv2.waitKey(0)
    return


def dewarp():
    return


# preprocessing
image_data, grayscale_mask = mask_green_ref_img("SampleImage.png")
# image_data, grayscale_mask = mask_green_ref_img("testimg2.png")
# mask = mask_green_ref_img("testimg2.png")


harris_corners(image_data, grayscale_mask)

# returns the mask of the green square in the image, use harris corners to detect and place corners

cv2.imshow("result", green_mask)
cv2.waitKey(0)


# Usage
port = 9999  # Specify the port to listen on

img_num = 0

# while True:
#     save_path = (
#         "imgs/received_image_" + str(img_num) + ".jpg"
#     )  # Specify the path to save the received image
#     receive_image(port, save_path)
#     img_num += 1