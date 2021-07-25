import cv2
import pytesseract
import numpy as np
from os import listdir
from os.path import isfile, join


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# config to filter digits
conf = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'


def getIndex(hPuzzle, wPuzzle, hStart, wStart, x, y, w, h):
    wSquare = wPuzzle/9
    hSquare = hPuzzle/9
    if (w-x) > wSquare or (h-y) > hSquare:
        raise ValueError("number larger than one square detected")
    horizontalIndex = int((x - wStart) // wSquare)
    verticalIndex = int(8 - (y - hStart) // hSquare)
    # print(horizontalIndex)
    # print("8 - ({y} - {h}) // {s} = {v}".format(y=y,h=hStart,s=hSquare,v=verticalIndex))
    horizontalIndex2 = int((w - wStart) // wSquare)
    verticalIndex2 = int(8 - (h - hStart) // hSquare)
    # print(horizontalIndex2)
    # print("8 - ({y} - {h}) // {s} = {v}".format(y=h,h=hStart,s=hSquare,v=verticalIndex2))
    if horizontalIndex != horizontalIndex2 or verticalIndex != verticalIndex2:
        raise ValueError("number intersecting line detected")
    return horizontalIndex + verticalIndex * 9


def drawBox(checkedImage, originalImage, box, hImg, wImg, hPuzzle, wPuzzle, hStart, wStart, puzzleList):
    box = box.split(' ')
    x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
    # print("{x}, {y}, {w}, {h}".format(x=x, y=y, w=w, h=h))
    # print("x = {x}".format(x = box[0]))
    index = getIndex(hPuzzle, wPuzzle, hStart, wStart, x, y, w, h)
    if (puzzleList[index] != None):
        raise ValueError('two numbers in the same index detected')
    puzzleList[index] = box[0]
    cv2.rectangle(checkedImage, (x, hImg-y),
                  (w, hImg-h), (255, 255, 255), -1)
    cv2.rectangle(originalImage, (x, hImg-y), (w, hImg-h), (0, 0, 255), 1)
    cv2.putText(originalImage, box[0], (x, hImg-y+20),
                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)


def processImage(image):
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
    listOfHorizontalPoints = []
    for c in cnts:
        # print("c is {c}".format(c=c[0][0][0]))
        listOfHorizontalPoints.append(c[0][0][0])
        cv2.drawContours(image, [c], -1, (255, 255, 255), 2)
    wStart = min(listOfHorizontalPoints)
    wPuzzle = max(listOfHorizontalPoints) - wStart
    print("w is {w}".format(w=wPuzzle))

    # removing horizontal lines from image
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    detected_lines = cv2.morphologyEx(
        thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(
        detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    listOfVerticalPoints = []
    for c in cnts:
        # print("c2 is {c}".format(c=c[0][0][1]))
        listOfVerticalPoints.append(c[0][0][1])
        cv2.drawContours(image, [c], -1, (255, 255, 255), 2)
    hStart = min(listOfVerticalPoints)
    hPuzzle = max(listOfVerticalPoints) - hStart
    print("h is {w}".format(w=hPuzzle))

    thresh = 175
    processedImage = cv2.threshold(
        image, thresh, 255, cv2.THRESH_BINARY)[1]
    processedImage = cv2.cvtColor(processedImage, cv2.COLOR_BGR2RGB)
    return processedImage, wStart, wPuzzle, hStart, hPuzzle


def readImage(name):

    link = './images/' + name
    original_image = cv2.imread(link)

    processedImage, wStart, wPuzzle, hStart, hPuzzle = processImage(original_image.copy())
    hImg, wImg = processedImage.shape[0], processedImage.shape[1]

    # print(pytesseract.image_to_string(image, config=conf))

    print(name)
    puzzleList = [None] * 81

    boxes = pytesseract.image_to_boxes(processedImage, config=conf)
    for box in boxes.splitlines():
        drawBox(processedImage, original_image, box, hImg, wImg, hPuzzle,
                wPuzzle, hStart, wStart, puzzleList)

    # checked_image would be a full white image if all numbers are detected
    # below checks if checked_image is white
    if np.mean(processedImage) <= 254.9:
        for num in range(3):
            newBoxes = pytesseract.image_to_boxes(processedImage, config=conf)
            for newBox in newBoxes.splitlines():
                drawBox(processedImage, original_image,
                        newBox, hImg, wImg, hPuzzle, wPuzzle, hStart, wStart, puzzleList)

            if np.mean(processedImage) > 254.9:
                break
            processedImage = cv2.erode(processedImage, (3, 3), iterations=1)

        if np.mean(processedImage) <= 254.9:
            print(np.mean(processedImage))
            raise ValueError("puzzle not fully read")

    print(puzzleList)
    cv2.imshow(name, original_image)
    # cv2.imshow(name + " check", processedImage)


def main():
    mypath = "./images"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for filename in onlyfiles:
        try:
            readImage(filename)
        except ValueError as err:
            print(err.args)


main()

cv2.waitKey(0)
