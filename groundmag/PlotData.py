import numpy as np
import matplotlib.pyplot as plt
from .ReadData import ReadData
import DateTimeTools as TT
from .UTPlotLabel import UTPlotLabel

def PlotData(Station,Date,ut=None,fig=None,maps=[1,1,0,0],comp=['Bx','By','Bz','Bm'],high=None,low=None,nox=False):
	'''
	
	'''
	
	#create title string
	title = Station.upper()
	
	#Read data
	data = ReadData(Station,Date)
	
	#create a continuous time axis
	ud = np.unique(data.Date)
	nd = ud.size
	utc = np.copy(data.ut)
	for i in range(0,nd):
		dd = TT.DateDifference(ud[0],ud[i])
		use = np.where(data.Date == ud[i])[0]
		utc[use] += dd*24.0
	
	
	#filter data
	if (not high is None) or (not low is None):
		dt,ct = np.unique((utc[1:]-utc[:-1])*3600.0,return_counts=True)
		inter = dt[ct.argmax()]
		if low is None:
			low = inter
		if high is None:
			high = inter
		Bx = TT.lsfilter(data.Bx,high,low,inter)
		By = TT.lsfilter(data.By,high,low,inter)
		Bz = TT.lsfilter(data.Bz,high,low,inter)
		title += ': low = {:3.1f} s, high = {:3.1f} s'.format(np.float32(low),np.float32(high))
	else:
		Bx,By,Bz = data.Bx,data.By,data.Bz

	
	#cut the data down to within ut range
	if not ut is None:
		if np.size(Date) == 2:
		#	use = np.where(((data.Date == Date[0]) & (data.ut >= ut[0])) |
		#					((data.Date > Date[0]) & (data.Date < Date[1])) |
		#					((data.Date == Date[1]) & (data.ut <= ut[1])))[0]
			utr = [ut[0],ut[1]+TT.DateDifference(Date[0],Date[1])*24.0]
			use = np.where((utc >= utr[0]) & (utc <= utr[1]))[0]
			
		else:
			use = np.where((data.ut >= ut[0]) & (data.ut <= ut[1]))[0]
			utr = ut
		utc = utc[use]
		data = data[use]
		Bx = Bx[use]
		By = By[use]
		Bz = Bz[use]
	#utrange = [np.min(utc),np.max(utc)]
	utrange = utr
	
	#component data and color
	Bm = np.sqrt(Bx**2 + By**2 + Bz**2)
	cmpcol = {	'Bx':	(Bx,[1.0,0.0,0.0],'$B_x$'),
				'By':	(By,[0.0,1.0,0.0],'$B_y$'),
				'Bz':	(Bz,[0.0,0.0,1.0],'$B_z$'),
				'Bm':	(Bm,[0.0,0.0,0.0],'$\pm|B|$')}
	
	#create the plot window and axes
	if fig is None:
		fig = plt
		fig.figure()
	ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))

	#plot data
	if isinstance(comp,str):
		comp = [comp]
	nc = np.size(comp)
	for c in comp:
		B,col,lab = cmpcol[c]
		ax.plot(utc,B,color=col,label=lab)
		if c == 'Bm':
			ax.plot(utc,-B,color=col)
	#ylabel
	ax.set_ylabel('$B$ (nT)')
	
	#sort UT axis
	ax.set_xlim(utrange)
	UTPlotLabel(ax,'x')
	ax.set_xlabel('UT')
	
	#add the title
	ax.text(0.02,0.95,title,transform=ax.transAxes)
	
	#legend
	ax.legend()
	
	
	return ax
