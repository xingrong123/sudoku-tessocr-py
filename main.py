import cv2
import pytesseract


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# config to filter digits
conf = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'


def hello(name):
    link = './images/' + name + '.png'
    image = cv2.imread(link)

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
    for c in cnts:
        cv2.drawContours(image, [c], -1, (255, 255, 255), 2)

    # removing horizontal lines from image
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    detected_lines = cv2.morphologyEx(
        thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(
        detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(image, [c], -1, (255, 255, 255), 2)

    thresh = 175
    image = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)[1]

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hImg, wImg = image.shape[0], image.shape[1]

    # print(pytesseract.image_to_string(image, config=conf))

    boxes = pytesseract.image_to_boxes(image, config=conf)

    print('height = {hImg}, width = {wImg}'.format(hImg=hImg, wImg=wImg))

    for box in boxes.splitlines():
        box = box.split(' ')
        # print(box)
        x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
        cv2.rectangle(image, (x, hImg-y), (w, hImg-h), (0, 0, 255), 1)
        cv2.putText(image, box[0], (x, hImg-y+20),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)

    cv2.imshow(name, image)
    # cv2.imshow(name + " gray", gray)


hello('sudokuEasy1')
hello('sudokuEasy2')
hello('sudokuMedium1')
hello('sudokuMedium2')
hello('sudokuHard1')
hello('sudokuHard2')
hello('sudokuExpert1')
hello('sudokuExpert2')


cv2.waitKey(0)
