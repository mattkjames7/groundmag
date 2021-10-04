import numpy as np
from . import Globals
import datetime
import DateTimeTools as TT
import aacgmv2

def GetStationInfo(Station=None,Date=None):
	
	
	if Station is None:
		out = Globals.Stations
	else:
		use = np.array([np.where(Globals.Stations.Code == Station.upper())[0][0]])
		out = Globals.Stations[use]

	if not Date is None:
		yr,mn,dy = TT.DateSplit(Date)
		dt = datetime.datetime(year=yr[0],month=mn[0],day=dy[0])
		for i in range(out.size):
			out.mlat[i],out.mlon[i],_ = aacgmv2.convert_latlon(out.glat[i],out.glon[i],0.0,dt,method_code='G2A')
			
	return out
