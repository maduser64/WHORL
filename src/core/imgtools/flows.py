# FLOWS.PY --- Tools to extract gradient flows from an image.

import cv2
import numpy as np

def get_flows(img):
	"""
	Get a list of flows
	"""
	pass

def get_high_curvature(img):
	"""
	Get a list of high-curvature points.
	"""
	pass

def get_gradient(img):
	"""
	Get the gradient of an image.
	"""
	return cv2.Laplacian(img,cv2.CV_64F)