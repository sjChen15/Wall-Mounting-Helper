import socket
import cv2
import numpy as np


import logging

import os


def get_filename_from_path(filepath):
    # Use os.path.basename() to get the filename from the path
    filename = os.path.basename(filepath)
    return filename


# add logging to math engine
# Create a logger
logger = logging.getLogger(__name__)


# Set the logging level (choose from DEBUG, INFO, WARNING, ERROR, CRITICAL)
logger.setLevel(logging.DEBUG)


# Create a file handler to write log messages to a file
file_handler = logging.FileHandler("math_engine.log")


# Create a formatter to specify the log message format
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)


# Add the file handler to the logger
logger.addHandler(file_handler)


# Define ref square color
lower_green = np.array(
    [30, 80, 40]
)  # Adjust this threshold based on your specific case
upper_green = np.array(
    [80, 255, 255]
)  # Adjust this threshold based on your specific case


# Save sensor data


# Save picture data


# Figure out transformations using it


# Read the user image


# Skew


# Send the image to the pi


def is_green(color):
    # Function to check if a color is green based on its HSV values
    green_range_low = np.array(
        [
            40,
            40,
            40,
        ]
    )  # Adjust these thresholds based on your specific case
    green_range_high = np.array(
        [
            80,
            255,
            255,
        ]
    )  # Adjust these thresholds based on your specific case

    print(color)

    if (
        color[0] >= lower_green[0]
        and color[0] <= upper_green[0]
        and color[1] >= lower_green[1]
        and color[1] <= upper_green[1]
        and color[2] >= lower_green[2]
        and color[2] <= upper_green[2]
    ):
        return True
    return False


def zoom_at(img, zoom=1, angle=0, coord=None):

    cy, cx = [i / 2 for i in img.shape[:-1]] if coord is None else coord[::-1]

    rot_mat = cv2.getRotationMatrix2D((cx, cy), angle, zoom)
    result = cv2.warpAffine(img, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR)

    return result


def find_transform_from_corners(corners):

    top_left = []
    top_right = []
    bottom_left = []
    bottom_right = []

    points = [corners[0][0], corners[1][0], corners[2][0], corners[3][0]]

    midpoint_x = (points[0][0] + points[1][0] + points[2][0] + points[3][0]) * 0.25
    midpoint_y = (points[0][1] + points[1][1] + points[2][1] + points[3][1]) * 0.25

    for p in points:
        x = p[0]
        y = p[1]

        if x < midpoint_x and y < midpoint_y:
            top_left = p

        if x > midpoint_x and y < midpoint_y:
            top_right = p

        if x > midpoint_x and y > midpoint_y:
            bottom_right = p

        if x < midpoint_x and y > midpoint_y:
            bottom_left = p

    pts1 = np.float32([top_left, top_right, bottom_left])

    print(pts1)

    # pts1 = np.float32([corners[0][0], corners[1][0], corners[2][0]])

    pts2 = np.float32([[0, 0], [50, 0], [0, 50]])

    M = cv2.getAffineTransform(pts1, pts2)
    M_inverse = cv2.getAffineTransform(pts2, pts1)

    return M, M_inverse


def find_corners_from_ref(ref_img_path):
    # Step 1: Read the image
    try:
        image = cv2.imread(ref_img_path)
    except cv2.error as e:
        logger.error("Unable to read ref image")

    # corners

    corners = []
    # set to be the minimum size of the green refrence square to avoid detecting small imperfections as
    # valid reference polygons
    max_poly_area = 100

    # Step 2: Preprocess the image
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Step 3: Find contours
    mask = cv2.inRange(hsv, lower_green, upper_green)

    #cv2.imshow("mask", mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Step 4: Filter green quadrilaterals
    for contour in contours:
        epsilon = 0.1 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) == 4:  # Check if the contour has four corners (a quadrilateral)
            # Get the average color of the contour to check if it's green
            x, y, _, _ = cv2.boundingRect(approx)

            area = cv2.contourArea(contour)

            print(area)

            hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            color = np.mean(hsv_img[y : y + 5, x : x + 5], axis=(0, 1))

            if True:
                # Step 5: Draw bounding box around the green quadrilateral
                cv2.drawContours(image, [approx], 0, (255, 0, 0), 2)

                if area > max_poly_area:
                    max_poly_area = area
                    corners = approx
                print(approx)

    # Display the result
    cv2.imshow("Green Quadrilateral Detection", image)
    cv2.waitKey(0)

    print(corners)

    return corners

    # rows, cols, ch = image.shape


# locate_green_quadrilateral("test2.png")


def find_transform_from_sensors(d, a):

    return 0, 0


def unskew_img(distance, accelerometer):
    ref_img_path = "C:/Users/shiji/OneDrive/Documents/Wall-Mounting-Helper/Hardware/imgs_received/pi_cam_img.jpg"
    # ref_img_path = "imgs_to_send/pi_cam_img.jpg"
    ref_image = cv2.imread(ref_img_path)

    # using corners for skew
    # comment out the other skew algorithm to use it
    # corners = find_corners_from_ref(ref_img_path)
    # M, M_inv = find_transform_from_corners(corners)

    # using distance and tilt for skew
    M, M_inv = find_transform_from_sensors(distance, accelerometer)

    rows, cols, ch = ref_image.shape
    # dst = cv2.warpAffine(ref_image, M, (cols, rows))

    # GET LATEST PICTURE FROM FOLDER
    dirpath = "C:/Users/shiji/OneDrive/Documents/Wall-Mounting-Helper/Hardware/imgs"
    valid_files = [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]

    background_img_path = "C:/Users/shiji/OneDrive/Documents/Wall-Mounting-Helper/Hardware/misc_imgs/bg.png"
    # background_img_path = "misc_imgs/bg.png"

    # user_image_path = "misc_imgs/10-L50-W80.png"

    user_image_path = max(valid_files, key=os.path.getmtime)

    usr_img_filename = get_filename_from_path(user_image_path)

    # usr_img_filename = "10-L100-W200.png"

    # get the length and width of the image from the file path
    usr_img_parse = usr_img_filename.split("-")
    print(usr_img_parse)
    len_str = usr_img_parse[1][1:] # desired size of user image in cm
    wid_str = usr_img_parse[2][1:].split(".")[0]

    print(int(len_str))
    print(wid_str)

    background_img = cv2.imread(background_img_path)
    user_image = cv2.imread(user_image_path)

    projector_width_unscaled = 1

    # resize user image to desired width and height
    usr_img_width_px = int(1920 * ((int(wid_str) * 0.010) / 2.0))
    usr_img_height_px = int(1080 * ((int(len_str) * 0.010) / (2.0*(1080/1920))))

    print(usr_img_width_px, usr_img_height_px)

    resized_img = cv2.resize(user_image, (usr_img_width_px, usr_img_height_px))

    x_offset = (background_img.shape[1] - resized_img.shape[1]) // 2
    y_offset = (background_img.shape[0] - resized_img.shape[0]) // 2

    background_img[
        y_offset : y_offset + resized_img.shape[0],
        x_offset : x_offset + resized_img.shape[1],
    ] = resized_img

    user_image = background_img

    # paste user image onto background grid

    # size of total projection
    throw_ratio = 88/120
    width_on_wall = distance * 0.01 * throw_ratio #size is of width of projection 

    if(width_on_wall ==0):
        width_on_wall = 2

    # desired total size in m
    desired_size = 2 #workspace projected size

    zoom = desired_size / width_on_wall #scaling factory for whole image

    zoomed_image = zoom_at(user_image, zoom)

    #cv2.imshow("user", zoomed_image)

    rows2, cols2, ch2 = user_image.shape
    # skew = cv2.warpAffine(user_image, M_inv, (cols2, rows2))

    # show image
    # cv2.imshow("Res", dst)
    # cv2.imshow("user", skew)
    #cv2.waitKey(0)

    cv2.imwrite(
        "C:/Users/shiji/OneDrive/Documents/Wall-Mounting-Helper/Hardware/imgs_to_send/processed.png",
        zoomed_image,
    )


# unskew_img(2, [0, 0, 0])


def process_image(dist, x_tilt, y_tilt, ref_img_path, user_img_path):

    M_inverse = find_transform_matrix(ref_img_path)


def locate_green_quadrilateral(image_path):
    # Step 1: Read the image
    image = cv2.imread(image_path)

    # corners

    corners = []

    # Step 2: Preprocess the image (you can apply additional techniques based on your image)
    # Step 2: Preprocess the image (you can apply additional techniques based on your image)
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the green color
    lower_green = np.array(
        [30, 80, 40]
    )  # Adjust this threshold based on your specific case
    upper_green = np.array(
        [50, 255, 255]
    )  # Adjust this threshold based on your specific case

    # Step 3: Find contours
    mask = cv2.inRange(hsv, lower_green, upper_green)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Step 4: Filter green quadrilaterals
    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) == 4:  # Check if the contour has four corners (a quadrilateral)
            # Get the average color of the contour to check if it's green
            x, y, _, _ = cv2.boundingRect(approx)

            hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            color = np.mean(hsv_img[y : y + 5, x : x + 5], axis=(0, 1))

            if True:
                # Step 5: Draw bounding box around the green quadrilateral
                cv2.drawContours(image, [approx], 0, (255, 0, 0), 2)
                corners = approx
                print(approx)

    # Display the result
    cv2.imshow("Green Quadrilateral Detection", image)
    cv2.waitKey(0)

    print(corners)

    pts1 = np.float32([corners[0][0], corners[1][0], corners[2][0]])

    pts2 = np.float32([[0, 0], [0, 200], [200, 200]])

    rows, cols, ch = image.shape
    M = cv2.getAffineTransform(pts1, pts2)
    M_inverse = cv2.getAffineTransform(pts2, pts1)
    dst = cv2.warpAffine(image, M, (cols, rows))

    user_image = cv2.imread("UserImage.png")

    zoomed_image = zoom_at(user_image, 1)

    cv2.imshow("zoom", zoomed_image)

    rows2, cols2, ch2 = zoomed_image.shape
    skew = cv2.warpAffine(zoomed_image, M_inverse, (cols2, rows2))

    # show image
    cv2.imshow("Res", dst)
    cv2.imshow("user", skew)

    cv2.waitKey(0)
