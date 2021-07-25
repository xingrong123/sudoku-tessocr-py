from typing import DefaultDict
from warnings import catch_warnings
import cv2
import pytesseract
import numpy as np
from os import listdir
from os.path import isfile, join


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# config to filter digits
conf = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'


def get_index(h_puzzle, w_puzzle, h_start, w_start, x, y, w, h):
    w_square = w_puzzle/9
    h_square = h_puzzle/9
    if (w-x) > w_square or (h-y) > h_square:
        raise ValueError("number larger than one square detected")
    horizontal_index = int((x - w_start) // w_square)
    vertical_index = int(8 - (y - h_start) // h_square)
    # print(horizontal_index)
    # print("8 - ({y} - {h}) // {s} = {v}".format(y=y,h=h_start,s=h_square,v=vertical_index))
    horizontal_index_2 = int((w - w_start) // w_square)
    vertical_index_2 = int(8 - (h - h_start) // h_square)
    # print(horizontal_index_2)
    # print("8 - ({y} - {h}) // {s} = {v}".format(y=h,h=h_start,s=h_square,v=vertical_index_2))
    if horizontal_index != horizontal_index_2 or vertical_index != vertical_index_2:
        raise ValueError("number intersecting line detected")
    return horizontal_index + vertical_index * 9


def draw_box(processed_image, original_image, box, h_img, w_img, h_puzzle, w_puzzle, h_start, w_start, puzzle_list):
    box = box.split(' ')
    x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
    # print("{x}, {y}, {w}, {h}".format(x=x, y=y, w=w, h=h))
    # print("x = {x}".format(x = box[0]))
    index = get_index(h_puzzle, w_puzzle, h_start, w_start, x, y, w, h)
    if (puzzle_list[index] != None):
        raise ValueError('two numbers in the same index detected')
    puzzle_list[index] = box[0]
    cv2.rectangle(processed_image, (x, h_img-y),
                  (w, h_img-h), (255, 255, 255), -1)
    cv2.rectangle(original_image, (x, h_img-y), (w, h_img-h), (0, 0, 255), 1)
    cv2.putText(original_image, box[0], (x, h_img-y+20),
                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)


def process_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # removing vertical lines from image
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
    detected_lines = cv2.morphologyEx(
        thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    cnts = cv2.findContours(
        detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    list_of_horizontal_points = []
    for c in cnts:
        # print("c is {c}".format(c=c[0][0][0]))
        list_of_horizontal_points.append(c[0][0][0])
        cv2.drawContours(image, [c], -1, (255, 255, 255), 2)
    w_start = min(list_of_horizontal_points)
    w_puzzle = max(list_of_horizontal_points) - w_start
    # print("w is {w}".format(w=w_puzzle))

    # removing horizontal lines from image
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    detected_lines = cv2.morphologyEx(
        thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(
        detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    list_of_vertical_points = []
    for c in cnts:
        # print("c2 is {c}".format(c=c[0][0][1]))
        list_of_vertical_points.append(c[0][0][1])
        cv2.drawContours(image, [c], -1, (255, 255, 255), 2)
    h_start = min(list_of_vertical_points)
    h_puzzle = max(list_of_vertical_points) - h_start
    # print("h is {w}".format(w=h_puzzle))

    thresh = 175
    processed_image = cv2.threshold(
        image, thresh, 255, cv2.THRESH_BINARY)[1]
    processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
    return processed_image, w_start, w_puzzle, h_start, h_puzzle


def format_puzzle_list(puzzle_list):

    puzzle_str = "["

    for item in puzzle_list:
        try:
            puzzle_str = puzzle_str + {
                None: "null,",
                '1': "1,",
                '2': "2,",
                '3': "3,",
                '4': "4,",
                '5': "5,",
                '6': "6,",
                '7': "7,",
                '8': "8,",
                '9': "9,"
            }[item]
        except:
            raise ValueError("invalid value detected in puzzle list", item)

        # match statement for python 3.10
        # match item:
        #     case None:
        #         str = str + "null,"
        #     case "1":
        #         str = str + item + ","
        #     case "2":
        #         str = str + item + ","
        #     case "3":
        #         str = str + item + ","
        #     case "4":
        #         str = str + item + ","
        #     case "5":
        #         str = str + item + ","
        #     case "6":
        #         str = str + item + ","
        #     case "7":
        #         str = str + item + ","
        #     case "8":
        #         str = str + item + ","
        #     case "9":
        #         str = str + item + ","
        #     case _:
        #         raise ValueError("unknown value in puzzle list")
    
    return puzzle_str[:-1] + "]"






def readImage(name):

    link = './images/' + name
    original_image = cv2.imread(link)

    processed_image, w_start, w_puzzle, h_start, h_puzzle = process_image(original_image.copy())
    h_img, w_img = processed_image.shape[0], processed_image.shape[1]

    # print(pytesseract.image_to_string(image, config=conf))

    print(name)
    puzzle_list = [None] * 81

    boxes = pytesseract.image_to_boxes(processed_image, config=conf)
    for box in boxes.splitlines():
        draw_box(processed_image, original_image, box, h_img, w_img, h_puzzle,
                w_puzzle, h_start, w_start, puzzle_list)

    # checked_image would be a full white image if all numbers are detected
    # below checks if checked_image is white
    if np.mean(processed_image) <= 254.9:
        for num in range(3):
            new_boxes = pytesseract.image_to_boxes(processed_image, config=conf)
            for new_box in new_boxes.splitlines():
                draw_box(processed_image, original_image,
                        new_box, h_img, w_img, h_puzzle, w_puzzle, h_start, w_start, puzzle_list)

            if np.mean(processed_image) > 254.9:
                break
            processed_image = cv2.erode(processed_image, (3, 3), iterations=1)

        if np.mean(processed_image) <= 254.9:
            print(np.mean(processed_image))
            raise ValueError("puzzle not fully read")

    # print(puzzle_list)
    # cv2.imshow(name, original_image)
    return format_puzzle_list(puzzle_list)
    # cv2.imshow(name + " check", processedImage)


def main():
    mypath = "./images"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for filename in onlyfiles:
        try:
            puzzle_list = readImage(filename)
            print(puzzle_list)
        except ValueError as err:
            print(err.args)


if __name__ == "__main__":
    main()


# cv2.waitKey(0)
