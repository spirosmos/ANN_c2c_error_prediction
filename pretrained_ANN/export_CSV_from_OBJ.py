from __future__ import division
import scipy as sp
import numpy as np
import igl
import math
from csv import writer,reader

def append_list_as_row(file_name, list_of_elem): 
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)
    write_obj.close()


def gaussian_curv(vertices, faces):
	k = igl.gaussian_curvature(vertices, faces)
	m = igl.massmatrix(vertices, faces, igl.MASSMATRIX_TYPE_VORONOI)
	diag = []
	for i in range(0,len(vertices)):
		if (m[i,i] != 0.0):
			diag.append(m[i,i])
		else:
			diag.append(1)
	diag = np.float64(diag)

	k = k/diag
	return k


def mean_curv(vertices, faces):
	l = igl.cotmatrix(vertices, faces)
	m = igl.massmatrix(vertices, faces, igl.MASSMATRIX_TYPE_VORONOI)
	minv = sp.sparse.diags(1 / m.diagonal())
	hn = -minv.dot(l.dot(vertices))
	h = np.linalg.norm(hn, axis=1)/2 	
	
	max_valueM = max(h)
	min_valueM = min(h)
	return h

def angleOnZ(n,acute):
	z = [0,0,1]
	all_angles = []
	for norm in n:
		angle = np.arccos(np.dot(z, norm) / (np.linalg.norm(z) * np.linalg.norm(norm)))
		if (acute == False): 	#DEGREES
			all_angles.append(math.degrees(angle))
			
		else:					#RADIANS
			all_angles.append(angle)
			

	if len(n) == 0:
		print("ERROR: No normals found")
		return None
	else:
		return all_angles

def bboxDist(v):
	print(v[:,0])
	min_x = np.min(v[:,0])
	max_x = np.max(v[:,0])

	min_y = np.min(v[:,1])
	max_y = np.max(v[:,1])

	min_z = np.min(v[:,2])
	max_z = np.max(v[:,2])

	bbdist = []
	bbdist_allPoint = []

	for i in range (0,len(v)):

		bbdist.append(max_x - v[i,0])		
		bbdist.append(max_y - v[i,1])
		bbdist.append(max_z - v[i,2])
		bbdist.append(v[i,0] - min_x)
		bbdist.append(v[i,1] - min_y)
		bbdist.append(v[i,2] - min_z)
	
		bbdist_allPoint.append(np.min(np.array(bbdist)))
		bbdist = []

	return bbdist_allPoint





def IGL_statistics(v, f):	
	vert_angles = [ [] for _ in range(len(v))]
	output_features = [ [] for _ in range(len(v))]
	angles = igl.internal_angles(v, f)

	angles = 360.0 * (angles / (2 * np.pi))

	for i in range (0,len(f)):
		vert_angles[f[i][0]].append(angles[i][0])
		vert_angles[f[i][1]].append(angles[i][1])
		vert_angles[f[i][2]].append(angles[i][2])
	for i in range (0,len(vert_angles)):

		avg = sum(vert_angles[i]) / len(vert_angles[i]) 
		output_features[i].append(avg)
		output_features[i].append(min(vert_angles[i]))
		output_features[i].append(max(vert_angles[i]))
	
	return output_features
	

def createDatalist(v, gaussC, meanC, inAng, normAng, bbd, verticesIDs, fileObj):
	row = []
	name = 'data_' + fileObj.replace('.obj','') + '.csv'
	append_list_as_row(name, ['x','y','z','gaussC','meanC','inAngleAVG','inAngleMin','inAngleMax','normalAnlgeOnZ','box_dist'])
	#for i in verticesIDs:
	for i in range(0,len(v)):
		row.append(v[i][0])
		row.append(v[i][1])
		row.append(v[i][2])
		row.append(gaussC[i])
		row.append(meanC[i])
		row.append(inAng[i][0])
		row.append(inAng[i][1])
		row.append(inAng[i][2])
		row.append(normAng[i])
		row.append(bbd[i])

		append_list_as_row(name, row)
		row = []




def main():
	#namesObj = np.array(["Woman_of_Pindos.obj"])
	namesObj = sys.argv[1:]


	for n in range (0,len(namesObj)):

		fileObj = namesObj[n]

		v, _, n, f, _, _ =igl.read_obj(fileObj)
		dataList = []
		
		bbd = bboxDist(v)				# len(v) X 1
		g = gaussian_curv(v,f) 			# len(v) X 1
		m = mean_curv(v,f) 				# len(v) X 1
		inAng = IGL_statistics(v,f) 	# len(v) X 3
		normAng = angleOnZ(n,False) 	# len(v) X 1

		sampling = np.random.random_integers(0,len(v)-1, 10000)

		createDatalist(v, g, m, inAng, normAng, bbd, sampling,fileObj)
		print("Data created for: " + fileObj)



if __name__ == '__main__':
	main()
	
