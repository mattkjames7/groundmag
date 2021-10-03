import numpy as np
from .ListFiles import ListFiles
from ._ReadCarisma import _ReadCanopus,_ReadCarisma1Hz,_ReadCarisma8Hz
from ._ReadIMAGE import _ReadIMAGE1s,_ReadIMAGEiaga
from .SaveData import SaveData
import os

def ConvertDir(indir,outdir,filetype,Compress=True):
	'''
	Convert the files within a directory.
	
	'''
	#get the appropriate conversion function/file extension
	ftypes = {  'canopus':('MAG',ConvertCanopus),
				'carisma1':('F01',ConvertCarisma1Hz),
				'carisma8':('',ConvertCarisma8Hz),
				'image1':('txt',ConvertIMAGE1Hz),
				'image':('iaga',ConvertIMAGEiaga)}
	ext,fun = ftypes(filetype)
	
	#list the files inside the input directory
	files,fnames = ListDir(indir,True)
	
	#check file extensions
	good = np.zeros(fnames.size,dtype='bool')
	if ext == '':
		ext = ['{:02d}'.format(i) for i in range(0,24)]
		for i in range(0,fnames.size):
			e = fnames[i][-3:]
			if e in ext:
				good[i] = True
				
		#remove the extensions and reduce to uniqe strings
		use = np.where(good)[0]
		files = files[use]	
		fnames = fnames[use]	
		
		newf = [f[:-3] for f in files]
		files = np.unique(newf)	
		
	else:
		elen = len(ext) + 1
		for i in range(0,fnames.size):
			e = fnames[i][-elen:]
			if e == ext:
				good[i] = True
				
		use = np.where(good)[0]
		files = files[use]
		n = files.size
		
	print('Found {:d} files to convert'.format(n))
	
	#convert each file
	for i in range(0,n):
		print('Converting file {:d} of {:d}'.format(i+1,n))
		fun(files[i],outdir,Compress)
	

def ConvertCanopus(fname,outdir,Compress=True):
	

	iname = fname.split('/')[-1].split('.')[0]
	date = iname[:8]
	year = iname[:4]
	stn = iname[8:].upper()
	
	#make sure the output directory exists
	odir = outdir+'/{:s}/'.format(year)
	if not os.path.isdir(odir):
		os.system('mkdir -pv '+odir)
	
	#now check that the output file doesn't exist	
	oname = odir + '{:s}-{:s}-5s.mag'.format(date,stn)

	if Compress:
		if os.path.isfile(oname+'.gz'):
			print('file exists...')
			return
	else:
		if os.path.isfile(oname):
			print('file exists...')
			return

	#read the data
	data = _ReadCanopus(fname)
	
	#save it
	SaveData(data,oname,Compress)
	
	
def ConvertCarisma1Hz(fname,outdir,Compress=True):
	

		
	iname = fname.split('/')[-1].split('.')[0]
	date = iname[:8]
	year = date[:4]
	stn = iname[8:].upper()
	
	#make sure the output directory exists
	odir = outdir+'/{:s}/'.format(year)
	if not os.path.isdir(odir):
		os.system('mkdir -pv '+odir)

	#now check that the output file doesn't exist
	oname = odir + '{:s}-{:s}-1s.mag'.format(date,stn)
	if Compress:
		if os.path.isfile(oname+'.gz'):
			print('file exists...')
			return
	else:
		if os.path.isfile(oname):
			print('file exists...')
			return
	
	#read the data
	data = _ReadCarisma1Hz(fname)
	
	#save it
	SaveData(data,oname,Compress)
	
def ConvertCarisma8Hz(fname,outdir,Compress=True):
	
	#this will require reading 24 files
	files = []
	for i in range(0,24):
		files.append(fname+'.{:02d}'.format(i))
		
		
	iname = fname.split('/')[-1]
	date = iname[:8]
	year = date[:4]
	stn = iname[8:].upper()
	
	
	#make sure the output directory exists
	odir = outdir+'/{:s}/'.format(year)
	if not os.path.isdir(odir):
		os.system('mkdir -pv '+odir)
	
	#now check that the output file doesn't exist
	oname = odir + '{:s}-{:s}-0.125s.mag'.format(date,stn)
	if Compress:
		if os.path.isfile(oname+'.gz'):
			print('file exists...')
			return
	else:
		if os.path.isfile(oname):
			print('file exists...')
			return
	
	#read the data
	data = []
	for i in range(0,24):
		try:
			tmp = _ReadCarisma8Hz(files[i])
			data.append(tmp)
		except:
			pass
	n = 0
	for d in data:
		n += d.size
	
	out = np.recarray(n,dtype=data[0].dtype)
	p = 0
	for d in data:
		out[p:p+d.size] = d
		p += d.size
	
	#save it
	SaveData(out,oname,Compress)	
	
	
def ConvertIMAGE1Hz(fname,outdir,Compress=True):
	
	#make sure the output directory exists
	if not os.path.isdir(outdir):
		os.system('mkdir -pv '+outdir)
		
	iname = fname.split('/')[-1].split('.')[0].split('_')
	date = iname[1]
	year = date[:4]
	stn = iname[0].upper()
	
	#make sure the output directory exists
	odir = outdir+'/{:s}/'.format(year)
	if not os.path.isdir(odir):
		os.system('mkdir -pv '+odir)
	
	#now check that the output file doesn't exist
	oname = odir + '{:s}-{:s}-1s.mag'.format(date,stn)
	if Compress:
		if os.path.isfile(oname+'.gz'):
			print('file exists...')
			return
	else:
		if os.path.isfile(oname):
			print('file exists...')
			return
	
	#read the data
	data = _ReadIMAGE1s(fname)
	
	#save it
	SaveData(data,oname,Compress)
	
def ConvertIMAGEiaga(fname,outdir,Compress=True):

	#get the file date
	iname = fname.split('/')[-1].split('.')[0].split('_')
	date = iname[1]
	year = date[:4]

	#read the data
	datadct = _ReadIMAGEiaga(fname)

	#make sure the output directory exists
	odir = outdir+'/{:s}/'.format(year)
	if not os.path.isdir(odir):
		os.system('mkdir -pv '+odir)
	
	#list the stations
	stn = list(datadct.keys())
	
	for s in stn:
		
		data,dt = datadct[s]

		oname = odir + '{:s}-{:s}-{:02d}s.mag'.format(date,s,dt)
		if os.path.isfile(oname+'.gz') or os.path.isfile(oname):
			print('file exists...')
		else:
			#save it
			SaveData(data,oname,Compress)					
	
