import numpy as np
import PyFileIO as pf


def _ReadIAGA2002(fname):
	'''
	This function will read the IAGA 2002 data format used by 
	INTERMAGNET.
	
	'''
	dtype = [	('Date','int32'),
				('ut','float64'),
				('Bx','float64'),
				('By','float64'),
				('Bz','float64')]
				
	dtype0 = [	('Date','object'),
				('ut','object'),
				('doy','int32'),
				('Bx','float64'),
				('By','float64'),
				('Bz','float64'),
				('Bm','float64')]
	
	lines = pf.ReadASCIIFile(fname)
	n = lines.size
	
	for i in range(0,n):
		if lines[i][0:4] == 'DATE':
			break
	lines = lines[i+1:]
	
	try:
		data = pf.ReadASCIIData(lines.tolist(),Header=False,dtype=dtype0)
	except:
		return np.recarray(0,dtype=dtype)
	n = data.size
	
	out = np.recarray(n,dtype=dtype)
	
	out.Bx = data.Bx
	out.By = data.By
	out.Bz = data.Bz
	
	out.Date = np.array([np.int32(D.replace('-','')) for D in data.Date])
		
	for i in range(0,n):
		h = np.int32(data.ut[i][0:2])
		m = np.int32(data.ut[i][3:5])
		s = np.float32(data.ut[i][6:])
		out.ut[i] = h + m/60 + s/3600.0


	badx = out.Bx > 90000.0
	bady = out.By > 90000.0
	badz = out.Bz > 90000.0
	bad = np.where(badx | bady | badz)[0]
	out.Bx[bad] = np.nan
	out.By[bad] = np.nan
	out.Bz[bad] = np.nan
		
		
	return out
