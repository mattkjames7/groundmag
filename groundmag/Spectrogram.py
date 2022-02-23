import numpy as np
import matplotlib.pyplot as plt
import wavespec as ws
from .GetData import GetData

def Spectrogram(Station,Date,wind,slip,**kwargs):
	
	ut = kwargs.get('ut',None)
	high = kwargs.get('high',None)
	low = kwargs.get('low',None)
	comp = kwargs.get('comp','Bx')
	
	#get the data
	data = GetData(Station,Date,ut,high,low)
	
	
	#get the spectrogram
	return ws.Spectrogram.Spectrogram(data.utc*3600.0,
						data[comp],wind,slip,**kwargs)
	
	

