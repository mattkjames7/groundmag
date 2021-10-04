import numpy as np
from . import Globals
import PyFileIO as pf
import os

def ReadDataIndex():
	
	dtype = [	('Date','int32'),
				('Station','object'),
				('Res','float32'),
				('File','object'),
				('SubDir','object')]

	fname = Globals.DataPath + 'index.dat'
	if os.path.isfile(fname):
		data = pf.ReadASCIIData(fname,Header=True,dtype=dtype)
	else:
		data = np.recarray(0,dtype=dtype)
		
	return data
