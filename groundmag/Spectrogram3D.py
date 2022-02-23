import numpy as np
import wavespec as ws
from .GetData import GetData

def Spectrogram3D(Station,Date,wind,slip,**kwargs):
	
	ut = kwargs.get('ut',None)
	high = kwargs.get('high',None)
	low = kwargs.get('low',None)
#	Freq = kwargs.get('Freq',None)
#	Method = kwargs.get('Method','FFT')
#	WindowFunction = kwargs.get('WindowFunction',None)
#	Param = kwargs.get('Param',None)
#	Detrend = kwargs.get('Detrend',True)
#	FindGaps = kwargs.get('FindGaps',True)
#	GoodData = kwargs.get('GoodData',None)
	if not 'CombineComps' in list(kwargs.keys()):
		kwargs['CombineComps'] = True
	
	#get the data
	data = GetData(Station,Date,ut,high,low)
	
	#get the spectrogram
	return ws.Spectrogram.Spectrogram3D(data.utc*3600.0,
				data.Bx,data.By,data.Bz,wind,slip,**kwargs)



