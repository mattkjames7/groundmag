import numpy as np
import groundmag as gm


def _ReadIndexFiles(path):
	
	files,fnames = gm.ListFiles(path,True)
	
	#extract the station names
	stn = [f.split('.')[0] for f in fnames]
	
	#read each file
	out = {}
	for i in range(0,files.size):
		out[stn[i]] = gm._ReadIndexFile(files[i])
		
	return out
	
	



def CompareDataDirs(path0,path1):
	'''
	This function will compare the magnetometer data from two different
	directories (it assumes that the index files are fully populated)
	
	A list of files to be removed from path0 will be provided (assuming 
	that files in path1 are duplicates which will replace them)
	
	'''
	
	#read the path indices
	idx0 = _ReadIndexFiles(path0)
	idx1 = _ReadIndexFiles(path1)

	#get both stations lists
	stn0 = np.array(list(idx0.keys()))
	stn1 = np.array(list(idx1.keys()))
	stn0.sort()
	stn1.sort()


	#list duplicates
	dups = []
	for s in stn0:
		if s in stn1:
			print('Checking {:s}'.format(s))
			si0 = idx0[s]
			si1 = idx1[s]
			d = np.zeros(si0.size,dtype='bool')
			for i in range(0,si0.size):
				print('\r{:07.3f}%'.format(100.0*(i+1)/si0.size),end='')
				if si0[i] in si1:
					d[i] = True
			print()
			ui = np.where(d)[0]
			f = path0 + si0.SubDir[ui] + si0.File[ui]
			dups.append(f)
	
	#combine everything
	dup = np.concatenate(dups)
	
	return dup
