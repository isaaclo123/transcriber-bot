"""Contains image handling and OCR code"""

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

def get_processed_image(img):
    """pre-processes an image for OCR

    :img: PIL image
    :returns: returns a preprocessed CV2 image
    :throws: RuntimeError indicating that the image could not be used

    code taken from
    https://stackoverflow.com/questions/24385714/detect-text-region-in-image-using-opencv#35078614

    """
    try:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img_gray, 180, 255, cv2.THRESH_BINARY) # pylint: disable=unused-variable
        img_final = cv2.bitwise_and(img_gray, img_gray, mask=mask)
        # for black text , cv.THRESH_BINARY_INV
        ret, new_img = cv2.threshold(img_final, 180, 255, cv2.THRESH_BINARY)


        """
        removing noise
        """


        # to manipulate the orientation of dilution , large x means
        # horizonatally dilating  more, large y means vertically dilating more
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

        # dilate , more the iteration more the dilation
        dilated = cv2.dilate(new_img, kernel, iterations=9)

        return dilated
    except BaseException as error:
        raise RuntimeError('Image could not be processed', error)

def get_processed_image_text(img): # pylint: disable=too-many-locals
    """finds blocks of text

    :img: a cv2 image object
    :returns: a string composed of the text found in the boxes appended together
    with "\n" characters
    :throws: RuntimeError indicating that the image could not be used

    code taken from
    https://stackoverflow.com/questions/24385714/
    detect-text-region-in-image-using-opencv#35078614

    """
    try:
        # preprocess image
        processed_image = get_processed_image(img)

        # finds image contours
        image, contours, hierarchy = cv2.findContours(processed_image, # pylint: disable=unused-variable
                                                      cv2.RETR_EXTERNAL,
                                                      cv2.CHAIN_APPROX_NONE)

        def _get_contour_text(contour):
            """helper method for getting a contour's text

            :contour: a cv2 contour object
            :returns: a contour's text

            """
            # get rectangle bounding contour
            [x, y, w, h] = cv2.boundingRect(contour)

            # Don't plot small false positives that aren't text
            if w < 35 and h < 35:
                return None

            # add text to final_text
            cropped_img = img[y : y + h, x : x + w]
            box_text = pytesseract.image_to_string(cropped_img)

            # Don't return string if it is only whitespace
            if box_text.isspace():
                return None

            return box_text

        final_text = ""

        for contour in contours:
            # add contour text to final text with newlines
            box_text = _get_contour_text(contour)
            if box_text:
                # if there is box text, add it
                final_text += "{}\n".format(box_text)
        # remove excess newlines
        final_text = final_text.lstrip().rstrip()

        return final_text
    except BaseException as error:
        raise RuntimeError('Image could not be processed', error)

def get_image_text(img_url):
    """gets preprocessed image text with pytessearct OCR

    :image_url: image url
    :returns: a string with the image's text

    """
    try:
        img = get_image(img_url)
        img_text = get_processed_image_text(img)
        return img_text
    except BaseException as error:
        # if error, return None
        print("Base exception: {error}".format(error=error))
        return None
