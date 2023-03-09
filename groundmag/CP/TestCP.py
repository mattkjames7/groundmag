import numpy as np
from ..ReadMagie import ReadMagie
import wavespec as ws
import DateTimeTools as TT
from scipy.interpolate import interp1d



def _interpdata(data):


	t = TT.ContUT(data[0].Date,0.0)[0] + np.arange(86400.0,dtype='float64')/3600.0

	out = np.recarray(t.size,data.dtype)
	out.utc = t
	out.Date,out.ut = TT.ContUTtoDate(t)

	for f in ['Bx','By','Bz']:
		fb = interp1d(data.utc,data[f],bounds_error=False,fill_value=np.nan)
		out[f] = fb(t)
		
	return out

def TestCP():
    
	eq = ReadMagie('dun')
	pl = ReadMagie('arm')

	eq = _interpdata(eq)
	pl = _interpdata(pl)

	tsec = (eq.utc - eq.utc[0])*3600.0


	return ws.DetectWaves.CPWavesFFT(tsec,eq.Bx,pl.Bx,1800.0,300.0,0.00125)