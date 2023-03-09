import numpy as np
import os
import datetime
import DateTimeTools as TT

def DownloadMagie(stn,DateRange=None,OutPath='/data/sol-ionosphere/mkj13/MagIE/'):
    
	if DateRange is None:
		date0 = 20130101
		td = datetime.datetime.today()
		date1 = np.int32(td.strftime('%Y%m%d'))

		DateRange = [date0,date1]

	dates = TT.ListDates(DateRange[0],DateRange[1])

	OutPath += '{:s}/'.format(stn)
	if not os.path.isdir(OutPath):
		os.makedirs(OutPath)

	for i,d in enumerate(dates):
		print('Downloading date {:d} of {:d} ({:d})'.format(i+1,dates.size,dates[i]))

		yy,mm,dd = TT.DateSplit(dates[i])
		url = 'https://data.magie.ie/{:4d}/{:02d}/{:02d}/txt/{:s}{:08d}.txt'.format(yy[0],mm[0],dd[0],stn.lower(),dates[i])
		fname = OutPath + '{:s}{:08d}.txt'.format(stn.lower(),dates[i])

		cmd = 'wget -O {:s} {:s}'.format(fname,url)
		os.system(cmd)