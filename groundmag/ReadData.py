import numpy as np
from . import Globals
import DateTimeTools as TT
from ._ReadBinary import _ReadBinary

def ReadData(Station,Date):
	'''
	
	'''
	
	#list dates
	if np.size(Date) == 1:
		dates = np.array([Date])
		nd = 1
	else:
		dates = []
		date = Date[0]
		while date <= Date[1]:
			dates.append(date)
			date = TT.PlusDay(date)
			
		nd = np.size(dates)
		
	#now load each file
	tmp = [object]*nd
	keys = list(Globals.Data.keys())
	for i in range(0,nd):
		#check if this file is already loaded
		label = '{:08d}-{:s}'.format(dates[i],Station.upper())
		
		if not label in keys:
			#load the file
			Globals.Data[label] = _ReadBinary(Station.upper(),dates[i])
		
		#retrieve this date from memory
		tmp[i] = Globals.Data[label]

	
	#now to combine dates
	if nd == 1:
		out = tmp[0]
	else:
		n = 0
		for i in range(0,nd):
			n += tmp[i].size
		out = np.recarray(n,dtype=tmp[0].dtype)
		p = 0
		for i in range(0,nd):
			s = tmp[i].size
			out[p:p+s] = tmp[i]
			p += s
			
	return out
	
