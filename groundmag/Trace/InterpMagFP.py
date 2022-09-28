import numpy as np
from .ReadMagTraces import ReadMagTraces
from ..Tools.GappyInterp import GappyInterp
import DateTimeTools as TT

def InterpMagFP(*args,Model='TS05'):
	'''
	Interpolate the trace footprints.
	
	Inputs
	======
	stn,Date,ut = *args
	
	OR
	
	stn,utc = *args
	
	stn : str
		Name of magnetometer
	Date : int32
		Date in format yyyymmdd
	ut : float
		Time in hours
	utc : float
		Continuous time
	
	
	'''
	
	if len(args) == 1:
		stn,utc = args
		Date,ut = TT.ContUTtoDate(utc)
	else:
		stn,Date,ut = args
		utc = TT.ContUT(Date,ut)
		
	DateLim = [Date.min(),Date.max()]
	
	T = ReadMagTraces(stn,DateLim,Model=Model)
		
	out = np.recarray(utc.size,dtype=T.dtype)
	out.Date = Date
	out.ut = ut
	out.utc = utc
	
	names = out.dtype.names
	for n in names:
		if not n in ['Date','ut','utc']:
			gi = GappyInterp(T.utc,T[n])
			out[n] = gi.Interp(utc)
			
	return out
