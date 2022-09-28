import numpy as np
from .TraceMagPair import TraceMagPair
from .. import Globals
import os
import DateTimeTools as TT
import RecarrayTools as RT

def SaveMagPairTraces(estn,pstn,Date,Model='TS05'):
	
	ut = np.arange(1440)/60.0
	
	T = TraceMagPair(estn,pstn,Date,ut,Model=Model)
	
	dtype = [	('Date','int32'),
				('ut','float32'),
				('utc','float64'),
				('GlonN','float32'),
				('GlonS','float32'),
				('GlatN','float32'),
				('GlatS','float32'),
				('MlonN','float32'),
				('MlonS','float32'),
				('MlatN','float32'),
				('MlatS','float32'),
				('GltN','float32'),
				('GltS','float32'),
				('MltN','float32'),
				('MltS','float32'),
				('MltE','float32'),
				('Lshell','float32')]
	data = np.recarray(1440,dtype=dtype)
		
	fields = data.dtype.names
	for f in fields:
		if hasattr(T,f):
			data[f] = getattr(T,f)
	
	data.utc = TT.ContUT(data.Date,data.ut)
	
	fpath = Globals.DataPath + 'Traces/{:s}/{:s}-{:s}/'.format(Model,estn,pstn)
	if not os.path.isdir(fpath):
		os.makedirs(fpath)
		
	fname = fpath + '{:08d}.bin'.format(Date)
	RT.SaveRecarray(data,fname,StoreDtype=True)
	
	
