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

def transform(img1,transformation):
	"""
	FIGURE OUT
	"""
	pass

def compute_transform(vec_1,vec_2):
	"""
	Given two vectors in R^2, compute the euclidean transformation
	taking vec_2 to vec_1.
	"""
	return {
		"shift" : vec_1 - vec_2,
		"rotation" : np.arccos(np.dot_product(vec_1 / np.norm(vec_1),
											  vec_2 / np.norm(vec_2)))
	}