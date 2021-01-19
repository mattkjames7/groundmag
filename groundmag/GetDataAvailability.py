import numpy as np
from .ListFiles import ListFiles
import DateTimeTools as TT
from . import Globals
import os

def GetDataAvailability(Station,Date=None):
	'''
	Scan for available data within $GROUNDMAG_DATA.
	
	Inputs
	======
	Station : str
		This should be the 3 or 4 character station code.
	Date : int
		This can be one of several things:-
		
		None: In this case, all dates for which there are data will be
		returned
		
		int : If a single integer date in the format yyyymmdd is 
		provided, then it will return this date and a boolean value 
		which is True if data exist on this day.
		
		[int,int] : If a 2-element date array/list is provided, then the
		function will create a list of all dates between Date[0] and
		Date[1] and return an array of all dates with an array of 
		booleans corresponding to each date, where True indicates 
		existing data.
		
		[int]*n : If a 3 or more element array of dates is provided then
		the function will only check the dates within this list.
		
	
	Returns
	=======
	dates : int
		Array of dates (if Date=None then all dates in this list 
		correspond to dates where data exists)
	exists : bool
		This array is only returned if the Date keyword is specified.
		This array contains boolean values for each date output in dates
		where True means the data exists, False means that there are no
		data for this date.
	
	
	'''

	#scan for all files
	files,fnames = ListFiles(Globals.DataPath,True)
	
	#reduce to just those for the specified station
	stn = Station.upper()
	isstn = np.array([(stn in f) and ('.mag.gz' in  f) for f in fnames])
	use = np.where(isstn)[0]
	fnames = fnames[use]
	nf = fnames.size

	#now list the dates
	fdates = np.array([np.int32(f[:8]) for f in fnames])
	fdates.sort()	
	
	
	

	#if Date is set to None, then look for all files for a station
	if Date is None:
		if use.size > 0:
			return fdates
	else:
		#otherwise, let's get a list of dates and check if they exist
		if np.size(Date) == 1:
			dates = np.array([Date])
			nd = 1
		elif np.size(Date) == 2:		
			dates = TT.ListDates(Date[0],Date[1])
			nd = dates.size
		else:
			dates = np.array(Date)
			nd = dates.size
		
		#loop through and check each one
		exists = np.zeros(nd,dtype='bool')
		for i in range(0,nd):
			exists[i] = dates[i] in fdates
			
		return dates,exists
