"""
align.py

expose function to align two fingerprints.
"""

# imports:
from focalvect import get_focal_vector
from ???.imgtools.euclidean import compute_transform, transform

def align_fingerprints(template_fp, query_fp,k4=6):
	"""
	COMMENTS HERE
	"""
	# ===== 1. calculate focal vectors of both images =====

	template_vec = get_focal_vector(template_fp,k4)
	query_vec = get_focal_vector(query_fp,k4)

	# ===== 2. get rigid transformation mapping q.v. to t.v. =====

	if (template_fp == query_fp):
		transformation = {
			"shift" : (0,0),
			"rotation" : 0
		}
	else:
		shift, rot = compute_transform(template_vec,query_vec)
		transformation = {
			"shift" : shift,
			"rotation" : rot
		}

	# ===== 3. return shifted and rotated query template =====

	return transform(query_fp,transformation)