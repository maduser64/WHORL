# EUCLIDEAN.PY --- Euclidean transformations on image arrays.

import cv2
import numpy as np

def translate(img,x,y):
	"""
	Translate an image matrix by (+x,+y).
	"""
	translation_matrix = np.float32([[1,0,x],[0,1,y]])

	return cv2.warpAffine(img,M,img.shape)

def rotate(img,phi):
	"""
	Rotate an image counter-clockwise by phi degrees, where
	phi ~ radians in the range 0 <= phi < 2pi.
	"""
	rows,cols = img.shape

	rotation_matrix = cv2.getRotationMatrix2D((cols/2, rows/2),90,1)

	return cv2.warpAffine(img,M,(cols,rows))