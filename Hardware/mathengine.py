import socket
import cv2
import numpy as np

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
        color[0] >= green_range_low[0]
        and color[0] <= green_range_high[0]
        and color[1] >= green_range_low[1]
        and color[1] <= green_range_high[1]
        and color[2] >= green_range_low[2]
        and color[2] <= green_range_high[2]
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

    pts2 = np.float32([[0, 0], [200, 0], [0, 200]])

    M = cv2.getAffineTransform(pts1, pts2)
    M_inverse = cv2.getAffineTransform(pts2, pts1)

    return M, M_inverse


def find_corners_from_ref(ref_img_path):
    # Step 1: Read the image
    image = cv2.imread(ref_img_path)

    # corners

    corners = []
    max_poly_area = 0

    # Step 2: Preprocess the image
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the green color
    lower_green = np.array(
        [30, 80, 40]
    )  # Adjust this threshold based on your specific case
    upper_green = np.array(
        [80, 255, 255]
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

            area = cv2.contourArea(contour)

            print(area)

            hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            color = np.mean(hsv_img[y : y + 5, x : x + 5], axis=(0, 1))

            if is_green(color):
                # Step 5: Draw bounding box around the green quadrilateral
                cv2.drawContours(image, [approx], 0, (255, 0, 0), 2)

                if area > max_poly_area:
                    corners = approx
                print(approx)

    # Display the result
    # cv2.imshow("Green Quadrilateral Detection", image)
    # cv2.waitKey(0)

    print(corners)

    return corners

    # rows, cols, ch = image.shape


# locate_green_quadrilateral("test2.png")


def unskew_img():
    ref_img_path = "imgs/pi_cam_img.jpg"

    ref_image = cv2.imread(ref_img_path)

    corners = find_corners_from_ref(ref_img_path)
    M, M_inv = find_transform_from_corners(corners)

    rows, cols, ch = ref_image.shape
    dst = cv2.warpAffine(ref_image, M, (cols, rows))

    user_image = cv2.imread("imgs/UserImage.png")

    # zoomed_image = zoom_at(user_image, 1)

    # cv2.imshow("zoom", zoomed_image)

    rows2, cols2, ch2 = user_image.shape
    skew = cv2.warpAffine(user_image, M_inv, (cols2, rows2))

    # show image
    # cv2.imshow("Res", dst)
    # cv2.imshow("user", skew)
    # cv2.waitKey(0)

    cv2.imwrite("imgs_to_send/processed.png", skew)


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
