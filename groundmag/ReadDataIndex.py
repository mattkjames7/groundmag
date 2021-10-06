import numpy as np
from . import Globals
import PyFileIO as pf
import os
from .ListFiles import ListFiles

def ReadDataIndex():
	
	# list all of the files within the index directory
	path = Globals.DataPath + 'Index/'
	if not os.path.isdir(path):
		os.system('mkdir -pv '+path)
	files,fnames = ListFiles(path,True)
	
	#extract the station names
	stn = [f.split('.')[0] for f in fnames]
	
	#read each file
	out = {}
	for i in range(0,files.size):
		out[stn[i]] = _ReadIndexFile(files[i])
		
	return out
	
	

	
def _ReadIndexFile(fname):
	'''
	This will be reading the index file for a single magnetometer 
	station.
	
	'''
	dtype = [	('Date','int32'),
				('Station','object'),
				('Res','float32'),
				('File','object'),
				('SubDir','object')]


	if os.path.isfile(fname):
		data = pf.ReadASCIIData(fname,Header=True,dtype=dtype)
	else:
		data = np.recarray(0,dtype=dtype)
		
	return data
