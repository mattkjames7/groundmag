import numpy as np
import os


#this is the base url for the files
url0 = 'https://space.fmi.fi/image/plasmon/{:s}/'

#list of available stations
stats = ['HAN','IVA','KEV','KIL','MAS','MEK','MUO','NUR','NUR2','OUJ','PEL','RAN','TAR']


def _DownloadHTMLNames(s):
	'''
	download the HTML page for a given station
	
	'''
	
	tmpfname = '{:s}.html'.format(s)
	url = url0.format(s)
	ret = os.system('wget --no-verbose '+url+' -O '+tmpfname)
	
	
	#read it
	f = open(tmpfname,'r')
	lines = f.readlines()
	n = np.size(lines)
	f.close()
	
	use = []
	for i in range(0,n):
		if '.txt.gz' in lines[i] and not '{:s}_.txt.gz'.format(s) in lines[i]:
			use.append(i)
	use = np.array(use)
	lines = np.array(lines)[use]
	n = lines.size
	
	names = []
	for i in range(0,n):
		ls = lines[i].split('href="')
		lss = ls[1].split('">')
		names.append(lss[0])
	names = np.array(names)
	return names
	
	
def DownloadStation(s):
	
	#get the names
	names = _DownloadHTMLNames(s)
	url = url0.format(s)
	n = names.size
	
	opath = 'data/{:s}/'.format(s)
	if not os.path.isdir(opath):
		os.system('mkdir -pv '+opath)
	
	#download each file
	for i in range(0,n):
		print('Downloading file {0} of {1}'.format(i+1,n))
		if not os.path.isfile(opath+names[i]):
			os.system('wget --no-verbose '+url+names[i]+' -O '+opath+names[i])
		
	
def DownloadAll():
	for s in stats:
		print('Station: {s}'.format(s))
		DownloadStation(s)


def DownloadIAGA():
	'''
	Download iaga IMAGE data (usually 10 or 60s)
	
	'''
	cmd = 'wget "https://space.fmi.fi/image/www/data_download_month.php?month={:06d}" -O 10s/image_{:06d}.iaga.tar'
	fname = '10s/image_{:06d}.iaga.tar'
	
	yr = np.arange(1982,2022,1)
	mn = np.arange(12) + 1

	ym = np.zeros(yr.size*mn.size,dtype='int32')
	for i in range(0,yr.size):
		ym[i*12:(i+1)*12] = yr[i]*100 + mn
		
	n = ym.size
	for i in range(0,n):
		print('File {0} of {1}'.format(i+1,n))
		if os.path.isfile(fname.format(ym[i])):
			print('File exists, skipping')
		else:
			os.system(cmd.format(ym[i],ym[i]))
	
