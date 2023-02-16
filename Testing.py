import cv2
import numpy as np
import pyautogui
import math

DEBUG = True
DETECTED = False


def show_image(image):
    cv2.namedWindow("debug", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("debug", 600, 400)
    cv2.imshow("debug", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_image():
    # Take screenshot
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)

    if DEBUG:
        screenshot = cv2.imread("data\lichess2.jpg")

    if DEBUG:
        show_image(screenshot)

    return screenshot


def detect_chessboard():
    # Get the image
    screenshot = get_image()
    screenshot_orig = screenshot.copy()

    # Convert to grayscale
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    if DEBUG:
        show_image(gray)

    # Convert to BW
    (thresh, blackAndWhiteImage) = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)

    if DEBUG:
        show_image(blackAndWhiteImage)

    # Define chessboard size
    chessboard_size = (7, 7)

    # Find chessboard corners
    found, corners = cv2.findChessboardCorners(blackAndWhiteImage, chessboard_size, None)

    if not found:
        # If not detected can be because of the black background
        blackAndWhiteImage = cv2.bitwise_not(blackAndWhiteImage)
        found, corners = cv2.findChessboardCorners(blackAndWhiteImage, chessboard_size, None)

    # If not found loop the function
    if not found:
        print("Chessboard not found.")
        detect_chessboard()

    if DEBUG:
        # Draw chessboard corners
        cv2.drawChessboardCorners(screenshot, chessboard_size, corners, found)

    # Calculate corners distance
    sqsize = abs(corners[0][0][0] - corners[1][0][0])
    ptl = corners[0][0] - sqsize
    pbr = corners[len(corners) - 1][0] + sqsize

    # Calculate board ROI
    start_point = (int(math.ceil(ptl[0])), int(math.ceil(ptl[1])))
    end_point = (int(math.ceil(pbr[0])), int(math.ceil(pbr[1])))

    if DEBUG:
        # Paint board ROI
        roi = cv2.rectangle(screenshot, start_point, end_point, (255, 0, 0), 3)

        # Show screenshot with chessboard corners
        show_image(roi)

        # Test the board corners
        endloop = 0
        while endloop < 64:
            ps, pe = get_square(corners, sqsize, endloop)
            endloop = endloop + 1
            cv2.rectangle(screenshot, ps, pe, (255, 0, 150), 3)
            #show_image(screenshot)
            #ROI = screenshot_orig[ps[1]:pe[1], ps[0]:pe[0]].copy()
            #name = "data/Pieces/" + str(endloop) + ".png"
            #cv2.imwrite(name, ROI)
            ROI = screenshot_orig[ps[1]:pe[1], ps[0]:pe[0]].copy()
            res = image2fen(ROI)
            if res != "nope":
                print(image2fen(ROI))
    # Return chessboard corners
    return corners, roi


def get_square(corners, sqsize, code):
    ptl = (0, 0)
    pbr = (0, 0)

    # Translate the corners to chess squares
    # top left is 0 botom right is 63
    if 0 <= code <= 6:
        ptl = corners[code][0] - sqsize
        pbr = corners[code][0]
    elif code == 7:
        ptl = (corners[code - 1][0][0], corners[code - 1][0][1] - sqsize)
        pbr = (corners[code - 1][0][0] + sqsize, corners[code - 1][0][1])
    elif code == 8:
        ptl = corners[code - 1][0] - sqsize
        pbr = corners[code - 1][0]
    elif code == 16:
        ptl = corners[code - 2][0] - sqsize
        pbr = corners[code - 2][0]
    elif code == 24:
        ptl = corners[code - 3][0] - sqsize
        pbr = corners[code - 3][0]
    elif code == 32:
        ptl = corners[code - 4][0] - sqsize
        pbr = corners[code - 4][0]
    elif code == 40:
        ptl = corners[code - 5][0] - sqsize
        pbr = corners[code - 5][0]
    elif code == 48:
        ptl = corners[code - 6][0] - sqsize
        pbr = corners[code - 6][0]
    elif code == 56:
        ptl = (corners[code - 14][0][0] - sqsize, corners[code - 14][0][1])
        pbr = (corners[code - 14][0][0], corners[code - 14][0][1] + sqsize)
    elif 9 <= code <= 63:
        corrector = 0
        if 9 <= code <= 15:
            corrector = 9
        elif 17 <= code <= 23:
            corrector = 10
        elif 25 <= code <= 31:
            corrector = 11
        elif 33 <= code <= 39:
            corrector = 12
        elif 41 <= code <= 47:
            corrector = 13
        elif 49 <= code <= 55:
            corrector = 14
        else:
            corrector = 15
        ptl = corners[code - corrector][0]
        pbr = corners[code - corrector][0] + sqsize

    start_point = (int(math.ceil(ptl[0])), int(math.ceil(ptl[1])))
    end_point = (int(math.ceil(pbr[0])), int(math.ceil(pbr[1])))

    return start_point, end_point


def image2fen(chessboard):
    isdetected = "nope"

    # Convert to grayscale
    #chessboard = cv2.cvtColor(chessboard, cv2.COLOR_BGR2GRAY)

    # Load the chessboard image and the template images for each piece
    pawn_template = cv2.imread("data/Pieces/lichess/pawn.png")
    rook_template = cv2.imread("data/Pieces/lichess/rook.png")
    knight_template = cv2.imread("data/Pieces/lichess/knight.png")
    bishop_template = cv2.imread("data/Pieces/lichess/bishop.png")
    queen_template = cv2.imread("data/Pieces/lichess/queen.png")
    king_template = cv2.imread("data/Pieces/lichess/king.png")

    # Define a list of templates and corresponding names
    templates = [pawn_template, rook_template, knight_template, bishop_template, queen_template, king_template]
    names = ["pawn", "rook", "knight", "bishop", "queen", "king"]

    # Loop through each template
    for i in range(len(templates)):
        template = templates[i]
        name = names[i]

        # Perform template matching using cv2.matchTemplate()
        result = cv2.matchTemplate(chessboard, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # If a high match is found, draw a rectangle around the match
        if max_val > 0.7:
            top_left = max_loc
            bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
            cv2.rectangle(chessboard, top_left, bottom_right, (0, 0, 255), 2)

            # Put the name of the piece on the image
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(chessboard, name, (top_left[0], top_left[1] - 10), font, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
            isdetected = name
    # Show the final image with the detected pieces
    cv2.imshow("Detected Pieces", chessboard)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return isdetected


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Starting the app...")
    # Call the function to detect the chessboard
    detect_chessboard()
    print("Chess detected")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
