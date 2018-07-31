"""Contains image handling code"""

import requests
import numpy
import pytesseract
import cv2

def get_image(img_url):
    """Gets image from image url

    :img_url: image url
    :returns: returns a numpy Image
    :throws: RuntimeError indicating that the image could not be used

    """
    try:
        response = requests.get(img_url)
        img_arr = numpy.asarray(bytearray(response.content), dtype=numpy.uint8)
        img = cv2.imdecode(img_arr, -1) # 'Load it as it is'
        return img
    except BaseException as error:
        raise RuntimeError('Image could not be used', error)

def process_image(img):
    """pre-processes an image for OCR

    :img: PIL image
    :returns: returns a preprocessed CV2 image
    :throws: RuntimeError indicating that the image could not be used

    taken from
    https://www.pyimagesearch.com/2017/07/10/using-tesseract-ocr-python/

    """
    try:
        print("preprocessing image")
        # load the example image and convert it to grayscale
        processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # check to see if we should apply thresholding to preprocess the
        # image
        # if args["preprocess"] == "thresh":
        # processed_img = cv2.threshold(processed_img, 0, 255,
        #                              cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # make a check to see if median blurring should be done to remove
        # noise
        # elif args["preprocess"] == "blur":
        # processed_img = cv2.medianBlur(processed_img, 3)

        return processed_img
    except BaseException as error:
        raise RuntimeError('Image could not be processed', error)

def get_processed_image_text(img):
    """gets preprocessed image text with pytessearct OCR

    :img: processed CV2 image
    :returns: a string with the image's text
    :throws: RuntimeError indicating that the image could not be processed

    taken from
    https://www.pyimagesearch.com/2017/07/10/using-tesseract-ocr-python/

    """
    try:
        print("parsing text")
        text = pytesseract.image_to_string(img)
        return text
    except BaseException as error:
        raise RuntimeError('Image text OCR failed', error)

def get_image_text(img_url):
    """gets preprocessed image text with pytessearct OCR

    :image_url: image url
    :returns: a string with the image's text
    :throws: RuntimeError indicating that the image could not be processed

    taken from
    https://www.pyimagesearch.com/2017/07/10/using-tesseract-ocr-python/

    """
    try:
        img = get_image(img_url)
        processed_img = process_image(img)
        img_text = get_processed_image_text(processed_img)
        return img_text
    except BaseException as error:
        # if error, return empty string
        print("Base exception: {error}".format(error=error))
        return ""
