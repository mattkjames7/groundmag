import numpy as np
import PyFileIO as pf

def _ReadCanopus(fname):
	'''
	This will read the extracted 0.2 Hz Canopus data files with the file 
	name format 'yyyymmddSSSS.MAG'.
	
	'''
	dtype = [	('Date','int32'),
				('ut','float64'),
				('Bx','float64'),
				('By','float64'),
				('Bz','float64')]
				
	dtype0 = [	('dt','object'),
				('Bx','float64'),
				('By','float64'),
				('Bz','float64'),
				('nothing','object')]
	
	lines = pf.ReadASCIIfile(fname)
	n = lines.size
	
	for i in range(0,n):
		if lines[i][0] != '#':
			break
	lines = lines[i+1:]
	
	data = pf.ReadASCIIData(lines,Header=False,dtype=dtype0)

	
	out = np.recarray(n,dtype=dtype)
	
	out.Bx = data.Bx
	out.By = data.By
	out.Bz = data.Bz
	
	out.Date = np.array([np.int32(s[:8]) for s in data.dt])
	
	for i in range(0,n):
		h = np.int32(data.dt[i][8:10])
		m = np.int32(data.dt[i][10:12])
		s = np.int32(data.dt[i][12:14])
		out.ut[i] = h + m/60 + s/3600.0

	badx = out.Bx > 90000.0
	bady = out.By > 90000.0
	badz = out.Bz > 90000.0
	bad = np.where(badx | bady | badz)[0]
	out.Bx[bad] = np.nan
	out.By[bad] = np.nan
	out.Bz[bad] = np.nan
		
		
	return out

def _ReadCarisma1Hz(fname):
	'''
	This will read the extracted 1 Hz Carisma data files with the file 
	name format 'yyyymmddSSSS.F01'.
	
	'''
	dtype = [	('Date','int32'),
				('ut','float64'),
				('Bx','float64'),
				('By','float64'),
				('Bz','float64')]
				
	dtype0 = [	('dt','object'),
				('Bx','float64'),
				('By','float64'),
				('Bz','float64'),
				('nothing','object')]
	
	data = pf.ReadASCIIData(fname,Header=True,dtype=dtype0)

	n = data.size
	out = np.recarray(n,dtype=dtype)
	
	out.Bx = data.Bx
	out.By = data.By
	out.Bz = data.Bz
	
	out.Date = np.array([np.int32(s[:8]) for s in data.dt])
	
	for i in range(0,n):
		h = np.int32(data.dt[i][8:10])
		m = np.int32(data.dt[i][10:12])
		s = np.int32(data.dt[i][12:14])
		out.ut[i] = h + m/60 + s/3600.0
		
	badx = out.Bx > 90000.0
	bady = out.By > 90000.0
	badz = out.Bz > 90000.0
	bad = np.where(badx | bady | badz)[0]
	out.Bx[bad] = np.nan
	out.By[bad] = np.nan
	out.Bz[bad] = np.nan
		
	return out


def _ReadCarisma8Hz(fname):
	
	'''
	This format is different to the others
	
	
	'''
	dtype = [	('Date','int32'),
				('ut','float64'),
				('Bx','float64'),
				('By','float64'),
				('Bz','float64')]

	lines = pf.ReadASCIIFile(fname)[1:]
	
	nrec = lines.size//9
	n = 8*nrec
	data = np.recarray(n,dtype=dtype)
	
	dt = np.arange(8)*0.125
	for i in range(0,nrec):
		i0 = i*8
		i1 = (i+1)*8
		l0 = i*9
		s = lines[l0].split()
		data.Date[i0:i1] = np.int32(s[0])
		hh = np.int32(s[1][0:2])
		mm = np.int32(s[1][2:4])
		ss = np.int32(s[1][4:6])
		data.ut[i0:i1] = (hh + mm/60.0 + ss/3600.0) + dt
		
		for j in range(0,8):
			s = np.float64(lines[l0 + 1 + j].split())
			data.Bx[i0 + j] = s[0]
			data.By[i0 + j] = s[1]
			data.Bz[i0 + j] = s[2]
		
	badx = out.Bx > 90000.0
	bady = out.By > 90000.0
	badz = out.Bz > 90000.0
	bad = np.where(badx | bady | badz)[0]
	out.Bx[bad] = np.nan
	out.By[bad] = np.nan
	out.Bz[bad] = np.nan
		
	return out	
