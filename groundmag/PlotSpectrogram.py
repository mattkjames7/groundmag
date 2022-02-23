import numpy as np
import matplotlib.pyplot as plt
import wavespec as ws
from .GetData import GetData

def PlotSpectrogram(Station,Date,wind,slip,**kwargs):
	
	ut = kwargs.get('ut',None)
	high = kwargs.get('high',None)
	low = kwargs.get('low',None)
	coords = kwargs.get('coords','hdz')
	comp = kwargs.get('comp','Bx')
	FreqAxisUnits = kwargs.get('FreqAxisUnits','mHz')
		
	#get the data
	data = GetData(Station,Date,ut,high,low,coords=coords)
	
	if 'SpecData' in list(kwargs.keys()):
		Freq,Tspec,Pow = kwargs['SpecData']
		ax = ws.Spectrogram.SpectrogramPlotter(Tspec,Freq*1000.0,Pow,**kwargs)
		Nw = Tspec.size
		Spec = None
	else:
			
		#spectrogram
		if comp in ['Bx','By','Bz']:
			#plot the spectrogram
			ax,Nw,Freq,Spec = ws.Spectrogram.PlotSpectrogram(data.utc*3600.0,
												data[comp],wind,slip,**kwargs)
			Pow = Spec.Pow
		else:
			Nw,Freq,Spec = ws.Spectrogram.Spectrogram3D(data.utc*3600.0,
							data.Bx,data.By,data.Bz,wind,slip,**kwargs)
			
			kwargs['PlotType'] = comp[1:] + kwargs.get('PlotType','Pow') 
			print(kwargs['PlotType'])
			ax,Nw,Freq,Spec = ws.Spectrogram.PlotSpectrogram(Freq,Spec,**kwargs)
			Pow = Spec[kwargs['PlotType']]
		Tspec = Spec.Tspec
	
	#change the ylabel
	ax.set_ylabel('{:s}\n$f$ ({:s})'.format(Station.upper(),FreqAxisUnits))
	
	Threshold = kwargs.get('Threshold',0.0)
	LargestPeak = kwargs.get('LargestPeak',True)
	ShowPeaks = kwargs.get('ShowPeaks',True)
	
	pk = ws.DetectWaves.DetectWavePeaks(Tspec,Freq,Pow,Threshold,LargestPeak)
	
	if ShowPeaks:
		t = pk.t/3600.0
		ax.scatter(t,pk.f*1000.0,color='lime',marker='.')


	return ax,Nw,Freq,Spec
