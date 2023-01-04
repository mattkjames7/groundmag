import numpy as np
import DateTimeTools as TT
from .. import Globals
import RecarrayTools as RT
import os

def _ReadMagTraceFile(stn,Date,Model):
	
	fpath = Globals.DataPath + 'Traces/{:s}/{:s}/'.format(Model,stn)	
	fname = fpath + '{:08d}.bin'.format(Date)	
	
	if os.path.isfile(fname):
		try:
			out = RT.ReadRecarray(fname)
		except:
			out = None
	else:
		out = None
	return out
	

def ReadMagTraces(stn,Date,ut=[0.0,24.0],Model='TS05'):
	
	if np.size(Date) == 1:
		dates = np.array(Date).flatten()
	elif np.size(Date) > 2:
		dates = np.array(Date)
	else:
		dates = TT.ListDates(Date[0],Date[1])
		
	datalist = []
	nf = 0
	ne = 0
	
	for d in dates:
		tmp = _ReadMagTraceFile(stn,d,Model)
		if not tmp is None:
			datalist.append(tmp)
			nf += 1
			ne += tmp.size
			
	if ne > 0 and nf > 0:
		data = np.recarray(ne,dtype=tmp.dtype)
		p = 0
		for i in range(0,nf):
			tmp = datalist[i]
			data[p:p+tmp.size] = tmp
			p += tmp.size
	else:
		return None

	#limit time
	datelim = [dates.min(),dates.max()]
	utclim = TT.ContUT(datelim,ut)

	use = np.where((data.utc >= utclim[0]) & (data.utc <= utclim[1]))[0]
	data = data[use]

	return data

	
