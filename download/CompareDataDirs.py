import numpy as np
import groundmag as gm
import os

def _ReadIndexFiles(path):
	
	files,fnames = gm.ListFiles(path,True)
	
	#extract the station names
	stn = [f.split('.')[0] for f in fnames]
	
	#read each file
	out = {}
	for i in range(0,files.size):
		print(files[i])
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
	idx0 = _ReadIndexFiles(path0+'/Index/')
	idx1 = _ReadIndexFiles(path1+'/Index/')

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
			
			#create string arrays to compare with
			s0 = np.array(['{:s}{:d}{:f}'.format(si0.Station[i],si0.Date[i],si0.Res[i]) for i in range(0,si0.size)])
			s1 = np.array(['{:s}{:d}{:f}'.format(si1.Station[i],si1.Date[i],si1.Res[i]) for i in range(0,si1.size)])
			
			d = np.zeros(si0.size,dtype='bool')
			for i in range(0,si0.size):
				print('\r{:07.3f}%'.format(100.0*(i+1)/si0.size),end='')
				if s0[i] in s1:
					d[i] = True
			print()
			ui = np.where(d)[0]
			f = path0 + '/' + si0.SubDir[ui] + si0.File[ui]
			dups.append(f)
	
	#combine everything
	dup = np.concatenate(dups)
	
	return dup


def MoveFiles(path0,path1,mvpath):
	
	dup = CompareDataDirs(path0,path1)
	
	if not os.path.isdir(mvpath):
		os.system('mkdir -pv '+mvpath)
		
	print(os.path.isdir(path0))
	print(os.path.isdir(path1))
	print(os.path.isdir(mvpath))
		
	for i in range(0,dup.size):
		print('\rMoving file {:06d} of {:06d}'.format(i+1,dup.size),end='')
		#print()
		#print('mv '+dup[i]+' '+mvpath)
		#print(os.path.isfile(dup[i]))
		#print()
		os.system('mv '+dup[i]+' '+mvpath)
