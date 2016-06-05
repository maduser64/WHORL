"""

"""

# imports:
from core.imgtools.flows import get_high_curvature_pts
import numpy as np

def get_focal_vector(img,kappa,window=3,lbound=0.3):
	"""
	get_focal_vector takes an image and extracts the focal point from a fingerprint.
	Performs the following:
	1. Finds all the points of high curvature, P = p_1, ..., p_N
	2. For each point, compute it's voted focal point VOTE(p_i)
	3. For each point, compute the normal vector to the flow tangent u_i
	4. Compute the focal point as the centroid of voted focals
	5. Compute the mean curvature (`theta`) as the mean of the normals
	6. Return focal point(s).
	"""
	
	# 1) find all clusters of high curvature:
	# run function to extract array of high curvature points:
	high_curv_pts = get_high_curv_pts(img,window,lbound);
	
	# delete any row with all zeros:
	delete_zero_rows(high_curv_pts) # FIX THIS!!!
	
	# get number of points:
	num_points = np.shape(high_curv_pts)[0]

	# 2) for each point, compute voted focal point:
	focal_candidates = np.zeros((num_points,2))
	for p in range(0,num_points):
		pt = high_curv_pts[p,:]
		vote = compute_vote(pt[0],pt[1],pt[2],pt[3],pt[4],kappa)
		focal_candidates[p,0] = vote[0]
		focal_candidates[p,1] = vote[1]

	# 3) for each point, compute normal vector to flow tangent
	normals = zeros(num_points,2);
	for q in range(0,num_points):
		pt = high_curv_pts[q,:]
		tangent_flow = pt[4:5]
		norm_vec = ( -tangent_flow(2) , tangent_flow(1) )
		magnitude = np.norm(norm_vec)
		normals[q,:] = norm_vec / magnitude

	# 4) compute focal point as centroid of voted focals
	focal = np.sum(focal_candidates,1) / num_points

	# 5) compute mean curvature as mean of normals
	theta_sum = np.sum(normals,1)
	theta = theta_sum / np.norm(theta_sum)

	# 6) return focal points:
	return [ focal theta ]

def compute_vote(lbda,mu,omega,dx,dy,kappa):
	"""
	COMPUTEVOTE() computes the following:
	For (lambda, mu, omega, x, y) |-> votes for point at distance
	exp(kappa * omega) away from (lambda,mu) in the direction normal
	to (x,y).
	"""
	# 1) compute normal to (x,y):
	normal_vec = ( -dy / np.norm((dx,dy)) , dx / np.norm((dx,dy)) )

	# 2) compute appropriate distance away from (lambda,mu):
	dist = exp(kappa * omega)

	# 3) compute voted point:
	return ( lbda+(normal_vec[0]*dist) , mu+(normal_vec[1]*dist) )