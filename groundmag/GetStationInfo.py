import numpy as np
from . import Globals

def GetStationInfo(Station=None):
	
	
	if Station is None:
		return Globals.Stations
	else:
		use = np.where(Globals.Stations.Code == Station.upper())[0][0]
		return Globals.Stations[use]
