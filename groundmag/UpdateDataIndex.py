import numpy as np
from .ListFiles import ListFiles
from . import Globals
from .ReadDataIndex import ReadDataIndex
import RecarrayTools as RT
import PyFileIO as pf
from ._ReadBinaryFile import _ReadBinaryFile
import os

def UpdateDataIndex():
	
	#get current index
	idx = ReadDataIndex()	
	ni = idx.size
	
	#list the files in the data directory
	files,fnames = ListFiles(Globals.DataPath,True)
	nf = files.size
	print('Found {:d} files in $GROUNDMAG_DATA'.format(nf))
	
	#make sure that they all have the correct extension
	good = np.array([(('.mag' in f) or ('.mag.gz' in f)) for f in fnames])
	use = np.where(good)[0]
	files = files[use]
	fnames = fnames[use]
	nf = use.size
	
	#extract subdirectory
	ldp = len(Globals.DataPath)
	subdir = np.array([files[i][ldp:-len(fnames[i])] for i in range(0,nf)])
	
	#list those which exist in the directory, but not in the index
	#or those which have been removed
	new = np.zeros(nf,dtype='bool')
	dlt = np.zeros(ni,dtype='bool')
	for i in range(0,nf):
		print('\rChecking for new files ({:8.4f}%)'.format(100.0*(i+1)/nf),end='')
		new[i] = not (fnames[i] in idx.File) 
	print()
	for i in range(0,ni):
		print('\rChecking for new files ({:8.4f}%)'.format(100.0*(i+1)/idx.size),end='')
		dlt[i] = not (os.path.isfile(Globals.DataPath+idx.SubDir[i]+idx.File[i]))
	print()
	
	#remove deleted ones
	if idx.size > 0:
		keep = np.where(dlt == False)[0]
		idx = idx[keep]
		print('{:d} files removed'.format(dlt.size - keep.size))
	
	#add new ones
	new = np.where(new)[0]
	print('Adding {:d} files...'.format(new.size))
	
	files = files[new]
	fnames = fnames[new]
	subdir = subdir[new]
	dates = np.array([np.int32(f[:8]) for f in fnames])
	fnamese = np.array([f.split('.')[0] for f in fnames])
	fnamess = np.array([f.split('-') for f in fnamese])
	stns = np.array([f[1] for f in fnamess])
	nidx = np.recarray(new.size,dtype=idx.dtype)
	
	nidx.File = fnames
	nidx.Station = stns
	nidx.SubDir = subdir
	nidx.Date = dates
	
	
	for i in range(0,new.size):
		print('\rObtaining time resolution ({:8.4f}%)'.format(100.0*(i+1)/new.size),end='')
		if len(fnamess[i]) == 3:
			nidx[i].Res = np.float32(fnamess[i][2].replace('s',''))
		else:
			s = _ReadBinaryFile(files[i],ReturnSize=True)
			r = 86400/s
			if r > 1:
				r = np.round(r)
			nidx[i].Res = r
	print()
		
	idx = RT.JoinRecarray(idx,nidx)
	
	fname = Globals.DataPath + 'index.dat'
	pf.WriteASCIIData(fname,idx)
	
	Globals.DataIndex = idx
