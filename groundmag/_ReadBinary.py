import numpy as np
from . import Globals
import os
from .GetDataIndex import GetDataIndex
from ._ReadBinaryFile import _ReadBinaryFile

def _ReadBinary(Station,Date,PreferredRes='min',ReturnSize=False):
	'''
	Read binary mag data.
	
	'''
	#get the data index
	idx = GetDataIndex()
	idx = idx[Station]
	use = np.where((idx.Date == Date))[0]
	idx = idx[use]
	use = np.where((idx.Station == Station))[0]
	idx = idx[use]
	if use.size == 0:
		dtype = [('Date','int32'),('ut','float64'),('Bx','float64'),('By','float64'),('Bz','float64')]
		return np.recarray(0,dtype=dtype)
			
	
	if PreferredRes == 'min':
		use = np.argmin(idx.Res)
	else:
		dr = np.abs(idx.Res - PreferredRes)
		use = np.argmin(dr)
	use = np.array([use])
	idx = idx[use]
	
	data = _ReadBinaryFile(Globals.DataPath + idx[0].SubDir + idx[0].File,ReturnSize=ReturnSize)
	return data
	
def _ReadBinaryOld(Station,Date):
	'''
	Read binary mag data.
	
	'''
	#create a randomized temporary path
	tpath = Globals.TmpPath + '{:08d}/'.format(np.random.randint(0,99999999))
	os.system('mkdir -p '+tpath)	
	
	#find out the input file name
	year = Date//10000
	ifile = Globals.DataPath + '{:04d}/{:08d}-{:s}.mag.gz'.format(year,Date,Station.upper())
	
	#copy file
	tfile = tpath + '{:08d}-{:s}.mag.gz'.format(Date,Station.upper())
	os.system('cp '+ifile+' '+tfile)
	
	#extract the archive
	os.system('gunzip '+tfile)

	#read the binary file
	bfile = tpath + '{:08d}-{:s}.mag'.format(Date,Station.upper())
	dtype = [('Date','int32'),('ut','float64'),('Bx','float64'),('By','float64'),('Bz','float64')]
	f = open(bfile,'rb')
	n = np.fromfile(f,dtype='int32',count=1)[0]
	data = np.recarray(n,dtype=dtype)
	data.Date = Date
	data.ut = np.fromfile(f,dtype='float64',count=n)
	data.Bx = np.fromfile(f,dtype='float64',count=n)
	data.By = np.fromfile(f,dtype='float64',count=n)
	data.Bz = np.fromfile(f,dtype='float64',count=n)
	f.close()
	
	#remove the file
	os.system('rm '+bfile)
	os.system('rm -d '+tpath)
	
	return data
