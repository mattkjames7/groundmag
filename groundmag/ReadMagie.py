import numpy as np
import PyFileIO as pf
import DateTimeTools as TT

def ReadMagie(stn='dun',Date=20230227,path='/data/sol-ionosphere/mkj13/MagIE/'):

	fname = '{:s}{:08d}.txt'.format(stn.lower(),Date)
	if not path.endswith('/'):
		path += '/'
	path += '{:s}/'.format(stn.lower())
	fname = path + fname
	dtype = [('DateStr','object'),
	  			('utStr','object'),
				('Index','int32'),
				('Bx','float64'),
				('By','float64'),
				('Bz','float64')]
	
	data = pf.ReadASCIIData(fname,Header=True,dtype=dtype)

	n = data.size
	Date = np.zeros(n,dtype='int32')
	ut = np.zeros(n,dtype='float32')
	for i in range(0,n):
		s = data.DateStr[i].split('/')
		Date[i] = np.int32(s[2]+s[1]+s[0])
		t = data.utStr[i].split(':')
		ut[i] = np.float64(t[0]) + np.float64(t[1])/60 + np.float64(t[2])/3600.0

	dtype = [('Date','int32'),
	  			('ut','float32'),
				('utc','float64'),
				('Bx','float64'),
				('By','float64'),
				('Bz','float64')]
	
	out = np.recarray(n,dtype=dtype)

	out.Date = Date
	out.ut = ut
	out.utc = TT.ContUT(Date,ut)
	out.Bx = data.Bx
	out.By = data.By
	out.Bz = data.Bz
	
	return out