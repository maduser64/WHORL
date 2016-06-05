# FLOWS.PY --- Tools to extract gradient flows from an image.

import cv2
import numpy as np

def get_flows(theta_mat,point,max_length,step):
	"""
	Get a list of flows -- FIX THIS

function flow = getFlowCurves(Theta,pt,N,STEP)
GETFLOWCURVES() takes orientation field angles and a point and
returns a column vector 
PARAMETERS:
Theta       --- angles of orientation field matrix
pt          --- (x,y) point
N           --- max length of flow curve
STEP		--- step size

	"""
	# each row of `flow` is of the form
	# (x,y,theta,tangent_x,tangent_y)
	flow = np.zeros(max_length,5)

	# define variables that contain current point data:
	point_x = point[0]
	point_y = point[1]
	theta = -1 * interpolate_orientation(theta_mat,point[0],point[1]);
	grad_x =  cos(theta)
	grad_y =  sin(theta)

	# now load data into flow iteratively:
	for idx in range(0,N):
		# store current data in flows:
		flow[idx,:] = [ pt_x pt_y theta grad_x grad_y ]
		# update step -- get new points by moving in direction of flow:
		point_x = step * grad_x + point_x
		point_y = step * grad_y + point_y
		# get new angle and gradients:
		theta = interpOrientation(theta_mat,point_x,point_y)
		grad_x =  cos(theta)
		grad_y =  sin(theta)

		# exit loop if pt_x or pt_y leaves boundaries:
		if point_x < 1:
			break
		if point_x > size(theta_mat,2):
			break
		if point_y < 1:
			break
		if point_y > size(theta_mat,1):
			break

	return flow

def get_high_curvature_pts(img,window,lbound,flow_length=100,step=0.05,sample_width=30):
	"""
	Get a list of high-curvature points from a flow. --FIX THIS

	GETHIGHCURVPTS() takes a fingerprint image and returns a collection of
	points of high curvature, including the tangent to the flow curve at
	each point. Returns a collection of points
	P = {(lambda,mu,omega,x,y)}.
	@ fingerprint --- fingerprint template.
	@ window --- window is the window size with which to calculate the angle.
	             By default, set to 5.
	@ lbound --- the lower bound above which a curvature is considerd to be 'high';
	             by default, this is set to 0.3.
	"""
	# initialize output:
	points = np.zeros((1,5))

	# ===== 1. Orientation Field Estimation: =====

	# get orientation angles on integer values by computing gradient:
	theta_mat = get_gradient(img)

	# ===== 2. Flow Curve Extraction: =====

	# generate list of starting points:
	KK = 1:floor(size(fingerprint,2) / (2 * sample_width))
	LL = 1:floor(size(fingerprint,1) / sample_width)
	startPts_x = 1 + KK * sample_width
	startPts_y = 1 + LL * sample_width
	[p,q] = meshgrid(startPts_x , startPts_y)
	startPts = [ p(:) q(:) ]

	# loop over all starting points:
	for i in range(0,size(startPts,1)):
		# get starting point:
		s0 = startPts[idx,:]
		# get flow:
		flow = get_flow_curves(theta_mat,s0,flow_length,step)

		# ===== 3. Calculate Max Curvature Points: =====

		# get list of high curvature points from the flow
		# and append to output:
		for jdx in range( (window+1) , (np.shape((flow,1)) - window + 1) ):
			# get start/end of window slice:
			fst = flow[jdx-window,:]
			snd = flow[jdx+window,:]
			
			# get curvature btwn fst and snd:
			a = fst[4:5]
			b = snd[4:5]
			omega = 1 - dot(a,b)

			# append point if omega > lbound:
			if (omega > lbound):
				# new_data = [ x y omega dx dy ]:
				new_data = [ flow(jdx,1) flow(jdx,2) omega flow(jdx,4) flow(jdx,5) ]
				points = [points ; new_data ]

	return points


def get_gradient(img):
	"""
	Get the gradient of an image.
	"""
	return cv2.Laplacian(img,cv2.CV_64F)

def interpolate_orientation(theta_mat,x,y):
	"""
	Take theta_mat a matrix of angles and (...)

	ESTORIENTATION(FINGERPRINT_TEMPLATE) takes a fingerprint template
	and estimates the orientation field via the method listed in
	the paper 'Markov Random Fields for Directed Field Estimation'.
	Takes parameters (x,y) ~ floats and returns gradient.
	"""
	# 1) define floors of coordinates:
	m = min(max(np.floor(x),1),(np.shape(theta_mat)[1]-2))
	n = min(max(np.floor(y),1),(np.shape(theta_mat)[0]-2))

	# 2) get angles from surrounding integer points on the lattice:
	pt1 = theta_mat[m,n]
	pt2 = theta_mat[m,(n+1)]
	pt3 = theta_mat[(m+1),n]
	pt4 = theta_mat[(m+1),(n+1)]

	# 3) define change of variables:
	u0 = m + 1 - x # == 0 when x is integer
	v0 = n + 1 - y # == 0 when y is integer
	u1 = 1 - u0    # == 1 when x is integer
	v1 = 1 - v0    # == 1 when y is integer

	# define numerator:
	numer_sum = (u0 * v0 * np.sin(2 * pt1)) + ...
				(u0 * v1 * np.sin(2 * pt2)) + ...
				(u1 * v0 * np.sin(2 * pt3)) + ...
				(u1 * v1 * np.sin(2 * pt4))

	# define denominator:
	denom_sum = (u0 * v0 * np.cos(2 * pt1)) + ...
				(u0 * v1 * np.cos(2 * pt2)) + ...
				(u1 * v0 * np.cos(2 * pt3)) + ...
				(u1 * v1 * np.cos(2 * pt4))

	# define gradient as (1/2) * arctan(N/D):
	return 0.5 * np.atan(numer_sum / denom_sum)