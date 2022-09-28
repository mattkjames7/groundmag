import numpy as np
from .MagTracePos import MagTracePos
import PyGeopack as gp

def TraceMag(stn,Date,ut,Model='TS05'):
	
	
	#make sure the date and time are the same length
	if np.size(ut) > 1 and np.size(Date) == 1:
		Date = np.zeros(np.size(ut),dtype='int32') + Date
		
	#get the mag position
	x,y,z = MagTracePos(stn,Date,ut)

	#do the trace!
	T = gp.TraceField(x,y,z,Date,ut,Model=Model,CoordIn='GSE')
	
	return T
