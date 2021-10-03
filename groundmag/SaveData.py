import numpy as np
import os

def SaveData(data,fname,Compress=True):
	'''
	Save data to a binary file
	
	Inputs
	======
	data : numpy.recarray
		Magnetometer data
	fname : str
		File name (and path).
	Compress : bool
		If True, then it will be gzipped.
	
	'''
	
	#check that we have the correct fields
	dtn = data.dtype.names
	fld = ['ut','Bx','By','Bz']
	for f in fld:
		if not f in fld:
			print('{:s} field not found'.format(f))
			
	#open the file
	f = open(fname,'wb')
	np.int32(data.size).tofile(f)
	data.ut.astype('float64').tofile(f)
	data.Bx.astype('float64').tofile(f)
	data.By.astype('float64').tofile(f)
	data.Bz.astype('float64').tofile(f)
	f.close()
	
	#compress
	if Compress:
		os.system('gzip '+fname)
