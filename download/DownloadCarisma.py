import numpy as np
import os
import PyFileIO as pf
import DateTimeTools as TT

datapath = '/media/ssd/carisma/{:04d}/'
url0 = 'http://data.carisma.ca/FGM/1Hz/{:04d}/{:02d}/{:02d}/'

def _GetDateFiles(date):
	
	#split date
	yr = date//10000
	mn = (date % 10000)//100
	dy = date % 100
	
	#get the url to search
	url = url0.format(yr,mn,dy)
	
	#download it
	os.system('wget --no-verbose '+url+' -O tmp.html')
	
	#read it in
	files = []
	lines = pf.ReadASCIIFile('tmp.html')
	
	for l in lines:
		s = l.split("'")
		for ss in s:
			if ".F01.gz" in ss and not '<' in ss:
				files.append(ss)
				
	files = np.array(files)
	
	#delete tmp file
	os.system('rm tmp.html')
	
	#get the fnames
	fnames = []
	for f in files:
		s = f.split('/')
		fnames.append(s[-1])
	fnames = np.array(fnames)
	

	#output files
	ofiles = []
	opath = datapath.format(yr)
	if not os.path.isdir(opath):
		os.system('mkdir -pv '+opath)
	for f in fnames:
		o = opath + f
		ofiles.append(o)
	ofiles = np.array(ofiles)
	n = ofiles.size
	
	#download them
	for i in range(0,n):
		os.system('wget --no-verbose '+'http://data.carisma.ca'+files[i]+' -O '+ofiles[i])
	

def DownloadCarisma():
	
	date0 = 20131201
	date1 = 20211001
	
	dates = TT.ListDates(date0,date1)
	n = dates.size
	for i in range(0,n):
		print('Downloading date {0} of {1}'.format(i+1,n))
		_GetDateFiles(dates[i])
