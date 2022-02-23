import numpy as np
import wavespec as ws

def SpecPolarization(Freq,Spec,comps=['x','y'],Threshold=1.0):
	#combine the appropriate components
	P = Spec[comps[0]+comps[1]+'Pow']
	
	#now find the most powerful peak along the time axis
	pk = ws.DetectWaves.DetectWavePeaks(Spec.Tspec,Freq,P,Threshold,True)
	
	#get the amplitudes and phases
	Ax = Spec.xAmp[pk.tind,pk.find]
	Px = Spec.xPha[pk.tind,pk.find]
	
	Ay = Spec.yAmp[pk.tind,pk.find]
	Py = Spec.yPha[pk.tind,pk.find]
	
	Az = Spec.zAmp[pk.tind,pk.find]
	Pz = Spec.zPha[pk.tind,pk.find]
	
	Dir = Spec.kz[pk.tind,pk.find]
	
	pol = ws.Tools.Polarization2D(Ax**2,Px,Ay**2,Py,ReturnType='dict')

	return pk,pol


def FullSpecPolarization(Spec):
	'''
	Return the 2D polarization ellipses for a whole spectrogram.
	Assumes that polarization is calcualted using x and y components,
	with kz indicating handedness.
	
	'''
		
	#get the amplitudes and phases
	Ax = Spec.xAmp
	Px = Spec.xPha
	
	Ay = Spec.yAmp
	Py = Spec.yPha
	
	Az = Spec.zAmp
	Pz = Spec.zPha
	
	Dir = Spec.kz
	
	pol = ws.Tools.Polarization2D(Ax**2,Px,Ay**2,Py,ReturnType='dict')
	
	
	return pol
