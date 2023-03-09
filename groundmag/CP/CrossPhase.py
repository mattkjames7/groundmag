import numpy as np
import DateTimeTools as TT
from scipy.interpolate import interp1d
import wavespec as ws

def _interpdata(data):


	t = TT.ContUT(data[0].Date,0.0)[0] + np.arange(86400.0,dtype='float64')/3600.0

	out = np.recarray(t.size,data.dtype)
	out.utc = t
	out.Date,out.ut = TT.ContUTtoDate(t)

	for f in ['Bx','By','Bz']:
		fb = interp1d(data.utc,data[f],bounds_error=False,fill_value=np.nan)
		out[f] = fb(t)
		
	return out


class CrossPhase(object):
	def __init__(self,edata,pdata,Window=1800,Slip=300,Highpass=0.00125):

		self.edata = _interpdata(edata)
		self.pdata = _interpdata(pdata)

		tsec = (self.edata.utc - self.edata.utc[0])*3600.0

		tmp = ws.DetectWaves.CPWavesFFT(tsec,self.edata.Bx,self.pdata.Bx,Window,Slip,Highpass)

		for k in tmp:
			setattr(self,k,tmp[k])

		self.utax = TT.ContUT(self.edata[0].Date,0.0)[0] + self.Tax/3600.0
		self.fmhz = self.F*1000

	def Plot(self,param,**kwargs):
	
		scale = kwargs.get('scale',None)
		cmap = kwargs.get('cmap','gnuplot')
		flim = kwargs.get('flim',[0.0,100.0])
		zlabel = kwargs.get('zlabel','')
		P = getattr(self,param)

		ax = ws.Spectrogram.SpectrogramPlotter(self.utax,self.fmhz,P,cmap=cmap,scale=scale,zlabel=zlabel)

		ax.set_ylabel('$f$ (mHz)')
		ax.set_ylim(flim)
		TT.DTPlotLabel(ax)

		return ax
    