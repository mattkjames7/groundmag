import numpy as np
from . import Globals
import os

def _ReadBinaryFile(ifile,ReturnSize=False):
	'''
	Read binary mag data.
	
	'''
	#create a randomized temporary path
	tpath = Globals.TmpPath + '{:08d}/'.format(np.random.randint(0,99999999))
	os.system('mkdir -p '+tpath)	
	
	#find out the input file name
	fname = ifile.split('/')[-1]
	s = fname.split('.')[0].split('-')
	Date = np.int32(s[0])
	Station = s[1]
	
	#copy file
	tfile = tpath + fname
	os.system('cp '+ifile+' '+tfile)
	
	#extract the archive
	os.system('gunzip '+tfile)

	#read the binary file
	bfile = tpath + fname[:-3]
	dtype = [('Date','int32'),('ut','float64'),('Bx','float64'),('By','float64'),('Bz','float64')]
	
	if not os.path.isfile(bfile):
		return np.recarray(0,dtype=dtype)
	
	try:
		f = open(bfile,'rb')
		n = np.fromfile(f,dtype='int32',count=1)[0]
		if ReturnSize:
			f.close()
		else:
			data = np.recarray(n,dtype=dtype)
			data.Date = Date
			data.ut = np.fromfile(f,dtype='float64',count=n)
			data.Bx = np.fromfile(f,dtype='float64',count=n)
			data.By = np.fromfile(f,dtype='float64',count=n)
			data.Bz = np.fromfile(f,dtype='float64',count=n)
			f.close()
	except:
		return np.recarray(0,dtype=dtype)
	#remove the file
	os.system('rm '+bfile)
	os.system('rm -d '+tpath)
	
	if ReturnSize:
		return n
	else:
		return data
