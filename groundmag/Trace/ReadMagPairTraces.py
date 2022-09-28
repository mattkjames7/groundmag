import numpy as np
import DateTimeTools as TT
from .. import Globals
import RecarrayTools as RT
import os

def _ReadMagPairTraceFile(estn,pstn,Date,Model):
	
	fpath = Globals.DataPath + 'Traces/{:s}/{:s}-{:s}/'.format(Model,estn,pstn)	
	fname = fpath + '{:08d}.bin'.format(Date)	
	
	if os.path.isfile(fname):
		try:
			out = RT.ReadRecarray(fname)
		except:
			out = None
	else:
		out = None
	return out
	

def ReadMagPairTraces(estn,pstn,Date,Model='TS05'):
	
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
		tmp = _ReadMagPairTraceFile(estn,pstn,d,Model)
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
		return data
	else:
		return None
	

	
