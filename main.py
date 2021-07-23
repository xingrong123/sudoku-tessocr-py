import cv2
import pytesseract
import numpy as np


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# config to filter digits
conf = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'


def drawBox(checkedImage, originalImage, box, hImg):
    box = box.split(' ')
    x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])

    cv2.rectangle(checkedImage, (x, hImg-y),
                  (w, hImg-h), (255, 255, 255), -1)
    cv2.rectangle(originalImage, (x, hImg-y), (w, hImg-h), (0, 0, 255), 1)
    cv2.putText(originalImage, box[0], (x, hImg-y+20),
                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)


def readImage(name):

    link = './images/' + name + '.png'
    original_image = cv2.imread(link)
    processedImage = original_image.copy()
    gray = cv2.cvtColor(processedImage, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # removing vertical lines from image
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
    detected_lines = cv2.morphologyEx(
        thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    cnts = cv2.findContours(
        detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(processedImage, [c], -1, (255, 255, 255), 2)

    # removing horizontal lines from image
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    detected_lines = cv2.morphologyEx(
        thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(
        detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(processedImage, [c], -1, (255, 255, 255), 2)

    thresh = 175
    processedImage = cv2.threshold(
        processedImage, thresh, 255, cv2.THRESH_BINARY)[1]

    processedImage = cv2.cvtColor(processedImage, cv2.COLOR_BGR2RGB)
    checked_image = processedImage.copy()
    hImg, wImg = processedImage.shape[0], processedImage.shape[1]

    # print(pytesseract.image_to_string(image, config=conf))


    print(name)

    boxes = pytesseract.image_to_boxes(processedImage, config=conf)
    for box in boxes.splitlines():
        drawBox(checked_image, original_image, box, hImg)
        
    # checked_image would be a full white image if all numbers are detected
    # below checks if checked_image is white
    if np.mean(checked_image) <= 254.9:
        for num in range(3):
            newBoxes = pytesseract.image_to_boxes(checked_image, config=conf)
            for newBox in newBoxes.splitlines():
                drawBox(checked_image, original_image, newBox, hImg)

            if np.mean(checked_image) > 254.9:
                break
            checked_image = cv2.erode(checked_image, (3, 3), iterations=1)

        if np.mean(checked_image) <= 254.9:
            print(np.mean(checked_image))
            print("error")

    cv2.imshow(name, original_image)
    cv2.imshow(name + " check", checked_image)


readImage('sudokuEasy1')
readImage('sudokuEasy2')
readImage('sudokuMedium1')
readImage('sudokuMedium2')
readImage('sudokuHard1')
readImage('sudokuHard2')
readImage('sudokuExpert1')
readImage('sudokuExpert2')


cv2.waitKey(0)
