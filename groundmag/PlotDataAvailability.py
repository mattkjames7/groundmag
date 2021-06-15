import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from .GetDataAvailability import GetDataAvailability
import DateTimeTools as TT

months = ['J','F','M','A','M','J','J','A','S','O','N','D']


def PlotDataAvailability(Stations,Date,fig=None,maps=[1,1,0,0]):
	
	#get the data availability for each station
	ns = len(Stations)
	for i in range(0,ns):
		d,e = GetDataAvailability(Stations[i],Date)
		if i == 0:
			nd = d.size
			x = d
			grid = np.zeros((ns,nd),dtype='float32')
		grid[i] = np.float32(e)
	
	#Get the x-axis and y-axis
	xe = np.arange(nd+1)*1.0
	ye = np.arange(ns+1)*1.0

	xg,yg = np.meshgrid(xe,ye)

	#get axis limits
	xlim = [0,nd]
	ylim = [0,ns]
	
	#get all of the years and months
	yr,mn,dy = TT.DateSplit(x)
		
	#determine where the ticks go
	mtick = np.where((dy == 1))[0]
	ytick = np.where((dy == 1) & (mn == 1))[0]
	
	if ytick.size > 2:
		#use yearly ticks
		xticks = xe[ytick]
		xticklabels = ['{:04d}'.format(yr[yt]) for yt in ytick]
	else:
		xticks = xe[mtick]
		xticklabels = []
		for i in range(0,mtick.size):
			if mn[mtick[i]] == 1:
				tmp = '{:s}\n{:04d}'.format(months[mn[mtick[i]]-1],yr[mtick[i]])
			else:
				tmp = '{:s}'.format(months[mn[mtick[i]]-1])
			xticklabels.append(tmp)
	
	yticks = ye
	yticklabels = ['']*(ns+1)
	
	#get the scale
	scale = [0.0,1.0]
	
	#set norm
	norm = colors.Normalize(vmin=scale[0],vmax=scale[1])	
	
	if fig is None:
		fig = plt
		fig.figure()
	if hasattr(fig,'Axes'):	
		ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))
	else:
		ax = fig
		
	sm = ax.pcolormesh(xg,yg,grid,cmap='RdYlGn',norm=norm,zorder=1.0)

	#set limits
	ax.set_xlim(xlim)
	ax.set_ylim(ylim)

	#set ticks
	ax.xaxis.set_ticks(xticks)
	ax.xaxis.set_ticklabels(xticklabels)
	ax.yaxis.set_ticks(yticks)
	ax.yaxis.set_ticklabels(yticklabels)
	for i in range(0,ns):
		ax.text(-0.03,(0.5 + i)/ns,Stations[i].upper(),ha='center',va='center',transform=ax.transAxes)
	
	#plot a grid
	#horizontal lines between stations
	ax.hlines(ye,xlim[0],xlim[1],color=[0.0,0.0,0.0],zorder=4)
	#vertical lines every year
	ax.vlines(xe[ytick],ylim[0],ylim[1],color=[0.0,0.0,0.0],zorder=4,lw=2.0)
	
	if ytick.size <= 5:
		#vertical lines every month
		ax.vlines(xe[mtick],ylim[0],ylim[1],color=[0.0,0.0,0.0],zorder=4,linestyle=':')
		
	return ax
