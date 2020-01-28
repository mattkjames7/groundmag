import numpy as np
import matplotlib.pyplot as plt
from .Spectrum import Spectrum

def PlotSpectrum(Station,Date,ut=None,high=None,low=None,Method='FFT',WindowFunction=None,Param=None,Freq=None,comp=['Bx','By','Bz'],PlotType='power',fig=None,maps=[1,1,0,0]):
	
	#get the spectra
	Freq,Pow,Amp,Pha,Real,Imag = Spectrum(Station,Date,ut,high,low,Method,WindowFunction,Param,Freq,comp)
	
	#select the parameter to plot
	plotparams = {	'power':	Pow,
					'phase':	Pha,
					'amplitude':	Amp,
					'real':		Real,
					'imaginary':	Imag}
	P = plotparams[PlotType]
	
	#create the figure
	if fig is None:
		fig = plt
		fig.figure()
	ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))

	#component label and color
	cmpcol = {	'Bx':	([1.0,0.0,0.0],'$B_x$'),
				'By':	([0.0,1.0,0.0],'$B_y$'),
				'Bz':	([0.0,0.0,1.0],'$B_z$')}

	#plot each component
	nc = np.size(comp)
	if nc == 1:
		P = [P]
	l = np.min([np.size(P[0]),np.size(Freq)])
	for i in range(0,nc):
		c,lab = cmpcol[comp[i]]
		ax.plot(Freq[:l],P[i][:l],color=c,label=lab)
		
	
	ax.legend()

	#axis labels
	ax.set_xlabel('Frequency')
