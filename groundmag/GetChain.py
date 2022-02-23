import numpy as np
import DateTimeTools as TT
from .GetStationInfo import GetStationInfo
from .GetDataAvailability import GetDataAvailability


def GetLonChain(lat,dlat=5.0,lonr=[-180.0,360.0],Network=None,
				Date=None):
	'''
	Get a longitudinal chain of ground magnetometers.
	
	Inputs
	======
	lat : float
		Approximate magnetic latitude of magnetometers (degrees).
	dlat : float
		Maximum deviation from lat (degrees).
	lonr : list/numpy.ndarray
		2-element array/list denoting the minimum and maximum magnetic 
		longitudes of stations.
	Network : None|str
		If str then only stations from Network will be included in 
		the output.
	Date : None|int|list
		If set, stations will only be included if there are data on the
		specified date(s).
		
	Returns
	=======
	stns : numpy.recaray
		Stations which fit the above criteria.
	
	'''

	#get all of the stations
	stns = GetStationInfo()
	
	#find those which fit with lat and lon limits
	goodlat = (stns.mlat >= lat-dlat) & (stns.mlat <= lat+dlat)
	goodlon = (stns.mlon >= lonr[0]) & (stns.mlon <= lonr[1])
	use = np.where(goodlat & goodlon)[0]
	stns = stns[use]
	
	#check Network
	if isinstance(Network,str):
		net = Network.lower()
		if not net in stns.Network:
			print('Network "{:s}" not found'.format(Network))
		else:
			use = np.where(net == stns.Network)[0]
			stns = stns[use]
	else:
		if not Network is None:
			print('Network keyword should be a string, ignoring...')
	
	#check there are data for specific dates
	if not Date is None:
		ns = stns.size
		av = np.zeros(ns,dtype='bool')
		for i in range(0,ns):
			d,e = GetDataAvailability(stns.Code[i],Date=Date,Quiet=True)
			if e.any():
				av[i] = True
		use = np.where(av)[0]
		stns = stns[use]
		
	srt = np.argsort(stns.mlon)
	stns = stns[srt]
		
	return stns

def GetLatChain(lon,dlon=5.0,latr=[-90.0,90.0],Network=None,
				Date=None):
	'''
	Get a longitudinal chain of ground magnetometers.
	
	Inputs
	======
	lon : float
		Approximate magnetic longitude of magnetometers (degrees).
	dlon : float
		Maximum deviation from lon (degrees).
	latr : list/numpy.ndarray
		2-element array/list denoting the minimum and maximum magnetic 
		latitudes of stations.
	Network : None|str
		If str then only stations from Network will be included in 
		the output.
	Date : None|int|list
		If set, stations will only be included if there are data on the
		specified date(s).
		
	Returns
	=======
	stns : numpy.recaray
		Stations which fit the above criteria.
	
	'''

	#get all of the stations
	stns = GetStationInfo()
	print(stns.size)
	
	#find those which fit with lat and lon limits
	goodlon = (stns.mlon >= lon-dlon) & (stns.mlon <= lon+dlon)
	goodlat = (stns.mlat >= latr[0]) & (stns.mlat <= latr[1])
	use = np.where(goodlat & goodlon)[0]
	stns = stns[use]
	print(stns.size)
	#check Network
	if isinstance(Network,str):
		net = Network.lower()
		if not net in stns.Network:
			print('Network "{:s}" not found'.format(Network))
		else:
			use = np.where(net == stns.Network)[0]
			stns = stns[use]
	else:
		print('Network keyword should be a string, ignoring...')

	
	#check there are data for specific dates
	if not Date is None:
		ns = stns.size
		av = np.zeros(ns,dtype='bool')
		for i in range(0,ns):
			d,e = GetDataAvailability(stns.Code[i],Date=Date,Quiet=True)
			if e.any():
				av[i] = True
		use = np.where(av)[0]
		stns = stns[use]
		
	srt = np.argsort(stns.mlat)
	stns = stns[srt]
			
	return stns
