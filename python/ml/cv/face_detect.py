__author__ = 'xialei'
# -*- coding: UTF-8 -*-

import cv2.cv as cv
import cv2
import numpy as np
from PIL import Image, ImageDraw

def detectObjects(image):
    """Converts an image to grayscale and print the locations of any faces found"""

    grayscale = cv.CreateImage(cv.GetSize(image), 8, 1)
    cv2.cv.CvtColor(image, grayscale, cv2.cv.CV_BGR2GRAY)

    storage = cv.CreateMemStorage(0)

    cv.EqualizeHist(grayscale, grayscale)

    cascade = cv.Load('haarcascade_frontalface_default.xml')
    # face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    min_size = (20, 20)
    faces = cv.HaarDetectObjects(grayscale, cascade, storage, 1.1, 2, cv.CV_HAAR_DO_CANNY_PRUNING, min_size)

    result = []

    for f in faces:
        result.append((f.x, f.y, f.x+f.width, f.y+f.height))

    return result

# def grayscale(r, g, b):
#     return int(r* .3 + g* .59 + b* .11)

def process(infile, outfile):

    image = cv.LoadImage(infile)
    if image:
        faces = detectObjects(image)

    im = Image.open(infile)

    if faces:
        draw = ImageDraw.Draw(im)
        for f in faces:
            draw.rectangle(f, outline=(255, 0, 255))

        im.save(outfile, "JPEG", quality=100)
    else:
        print "Error: cannot detect faces on %s" % infile

if __name__ == "__main__":
    process('input.jpg', 'output.jpg')


