import numpy as np
from .ListFiles import ListFiles
from . import Globals
from .ReadDataIndex import ReadDataIndex
import RecarrayTools as RT
import PyFileIO as pf
from ._ReadBinaryFile import _ReadBinaryFile
import os

def _GetMagFiles():

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


	#get resolution and stations 
	stns,dates,Res = _GetFilenameInfo(fnames)
	ustns = np.unique(stns)
	
	#create a new index
	dtype = [	('Date','int32'),
				('Station','object'),
				('Res','float32'),
				('File','object'),
				('SubDir','object')]	
				
	nidx = {}
	
	for s in ustns:
		use = np.where(stns == s)[0]
		sidx = np.recarray(use.size,dtype=dtype)
		sidx.Date = dates[use]
		sidx.Station[:] = s
		sidx.Res = Res[use]
		sidx.File = fnames[use]
		sidx.SubDir = subdir[use]
		nidx[s] = sidx
		

	return nidx

def _GetFilenameInfo(fnames):
	nf = fnames.size
	fnamese = np.array([f.split('.')[0] for f in fnames])
	fnamess = np.array([f.split('-') for f in fnamese])
	dates = np.array([np.int32(f[0]) for f in fnamess])
	stns = np.array([f[1] for f in fnamess])
	Res = np.zeros(nf,dtype='float32')
	for i in range(0,nf):
		if len(fnamess[i]) == 3:
			Res[i] = np.float32(fnamess[i][2].replace('s',''))
		else:	
			Res[i] = -1
	
	return stns,dates,Res


def _CheckForNewFiles(idx,nidx,Verbose=True):


	#list those which exist in the directory, but not in the index
	#or those which have been removed
	nf = nidx.size
	new = np.zeros(nf,dtype='bool')
	new[:] = True
	if not idx is None:
		for i in range(0,nf):
			if Verbose:
				print('\rChecking for new files ({:8.4f}%)'.format(100.0*(i+1)/nf),end='')
			if (nidx.File[i] in idx.File):
				new[i] = False
		if Verbose:
			print()

	new = np.where(new)[0]
	print('Found {:d} files...'.format(new.size))
	if new.size == 0:
		return None
	
	return nidx[new]
	
def UpdateDataIndex(Station=None,UpdateResolution=True,Verbose=True):
	

				
	#get current index
	idx = ReadDataIndex()	
	ikeys = list(idx.keys())
	
	#list the files in the data directory
	nidx = _GetMagFiles()
	
	#loop through each staton
	if Station is None:
		ustns = list(nidx.keys())
	else:
		if isinstance(Station,list):
			ustns = Station
		else:
			ustns = [Station]
	ns = len(ustns)
	for i in range(0,ns):
		save = False
		s = ustns[i]
		print('Saving station {:d} of {:d}: {:s}'.format(i+1,ns,s))
	
		#reduce to new files
		if s in ikeys:
			idxs = idx[s]
		else:
			idxs = None
		
		sidx = _CheckForNewFiles(idxs,nidx[s],Verbose=Verbose)
	
		if sidx is None:
			sidx = idxs
		elif not idxs is None:
			sidx = RT.JoinRecarray(sidx,idxs)
			save = True
		else:
			save = True
		
		if UpdateResolution and not sidx is None:
			bad = np.where(sidx.Res <= 0)[0]
			if bad.size > 0:
				save = True
				for i in range(0,bad.size):
					if Verbose or (i == (bad.size-1)) or (i % 100 == 0):
						print('\rObtaining time resolution ({:8.4f}%)'.format(100.0*(i+1)/bad.size),end='')
					try:
						S = _ReadBinaryFile(Globals.DataPath + sidx.SubDir[bad[i]] + sidx.File[bad[i]],ReturnSize=True)
						r = 86400/S
						if r > 1:
							r = np.round(r)
						sidx.Res[bad[i]] = r
					except:
						print('Bad file: {:s}'.format(Globals.DataPath + sidx.SubDir[bad[i]] + sidx.File[bad[i]]))
						sidx.Res[bad[i]] = 0
				if Verbose:
					print()
		
		if save:	
			fname = Globals.DataPath + 'Index/{:s}.dat'.format(s.upper())
			pf.WriteASCIIData(fname,sidx)
	print('done')
	Globals.DataIndex = ReadDataIndex()	

	
