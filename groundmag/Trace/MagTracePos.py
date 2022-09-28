import numpy as np
from ..GetStationInfo import GetStationInfo
import PyGeopack as gp

def MagTracePos(stn,Date,ut):
	'''
	This function will return the Cartesian GSE coordinates of a 
	magnetometer. The coordinates used will actually be at an altitude 
	just slightly higher than 1 Re so that the trace will work.
	
	Inputs
	======
	stn : str
		Station code.
	Date : int
		Integer date in the format yyyymmdd.
	ut : float
		Time in hours.
		
	Returns
	=======
	x : float
		x-GSE (Re)
	y : float
		y-GSE (Re)
	z : float
		z-GSE (Re)
	
	
	'''
	
	# get the mag position in longitude and latitude
	info = GetStationInfo(stn)[0]
	
	#convert to x y and z
	lonrad = info.glon*np.pi/180.0
	latrad = info.glat*np.pi/180.0
	r = 1.01
	x0 = r*np.cos(latrad)*np.cos(lonrad)
	y0 = r*np.cos(latrad)*np.sin(lonrad)
	z0 = r*np.sin(latrad)
	
	#make sure that time and date are the same length as x
	nt = np.size(ut)
	if nt > 1 and np.size(Date) == 1:
		Date = np.zeros(nt,dtype='int32') + Date

	#make x, y and z the same length
	x0 = np.zeros(nt,dtype='float64') + x0
	y0 = np.zeros(nt,dtype='float64') + y0
	z0 = np.zeros(nt,dtype='float64') + z0

	#convert to GSE
	x,y,z = gp.Coords.GEOtoGSE(x0,y0,z0,Date,ut)
	
	return x,y,z

