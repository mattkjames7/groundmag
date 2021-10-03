import numpy as np
import PyFileIO as pf
import DateTimeTools as TT

def _iaga_station(ss):

	dtype = [	('Date','int32'),
				('ut','float64'),
				('Bx','float64'),
				('By','float64'),
				('Bz','float64')]
	
	n = np.size(ss)
	
	#date and time
	Date = np.array([np.int32(ss[i][48:56]) for i in range(0,n)])
	ut0 = np.array([(np.float32(ss[i][56:58]) + np.float64(ss[i][58:60])/60.0) for i in range(0,n)])
	
	dt = np.array([np.int32(ss[i][60:62]) for i in range(0,n)])
	rlen = np.array([np.int32(ss[i][4:7]) for i in range(0,n)])
	nb = dt*60//rlen
	
	data = np.recarray(np.int32(nb.sum()),dtype=dtype)
	
	p = 0
	for i in range(0,n):
		i0 = p
		i1 = p + nb[i]
		
		data.Date[i0:i1] = Date[i]
		data.ut[i0:i1] = ut0[i] + np.arange(nb[i])*dt[i]/3600.0
	
		sb = ss[i][159:-21]
		b = np.array([sb[i*7:(i+1)*7] for i in range(0,len(sb)//7)])
		B = np.float32(b.reshape((nb[i],3)))/10.0
		data.Bx[i0:i1] = B[:,0]
		data.By[i0:i1] = B[:,1]
		data.Bz[i0:i1] = B[:,2]
		p += nb[i]

	badx = data.Bx > 90000.0
	bady = data.By > 90000.0
	badz = data.Bz > 90000.0
	bad = np.where(badx | bady | badz)[0]
	data.Bx[bad] = np.nan
	data.By[bad] = np.nan
	data.Bz[bad] = np.nan
		

	return data

def _ReadIMAGEiaga(fname):
	'''
	
	Read the mess of a format that is iaga.
	Name format: 'image_yyyymmdd.iaga' (10s data)
	
	'''
	
	#read the data
	lines = pf.ReadASCIIFile(fname)
	s = lines[0]
	
	#output dict
	out = {}
	
	#split into records
	rlen = np.int32(s[:4])
	ss = np.array([s[i*rlen:(i+1)*rlen] for i in range(0,len(s)//rlen)])
	nr = len(ss)
	
	#get ID
	ID = np.array([ss[i][12:15] for i in range(0,nr)])
	IDu = np.unique(ID)
	
	for I in IDu:
		use = np.where(ID == I)[0]
		out[I] = _iaga_station(ss[use])
	

	
	return out
	
def _ReadIMAGE1s(fname):
	'''
	this is for reading the files with the name 'SSS_yyyymmdd.txt'
	
	'''
	
	dtype0 = [	('yr','int32'),
				('mn','int32'),
				('dy','int32'),
				('hh','int32'),
				('mm','int32'),
				('ss','int32'),
				('Bx','float64'),
				('By','float64'),
				('Bz','float64')]
								
	dtype = [	('Date','int32'),
				('ut','float64'),
				('Bx','float64'),
				('By','float64'),
				('Bz','float64')]
	
	data = pf.ReadASCIIData(fname,Header=False,dtype=dtype0)


	badx = data.Bx > 90000.0
	bady = data.By > 90000.0
	badz = data.Bz > 90000.0
	bad = np.where(badx | bady | badz)[0]
	data.Bx[bad] = np.nan
	data.By[bad] = np.nan
	data.Bz[bad] = np.nan
		
	n = data.size
	out = np.recarray(n,dtype=dtype)
	
	out.Date = TT.DateJoin(data.yr,data.mn,data.dy)
	out.ut = TT.HHMMtoDec(data.hh,data.mm,data.ss)
	
	out.Bx = data.Bx
	out.By = data.By
	out.Bz = data.Bz

	return out
