import numpy as np
from scipy.interpolate import interp1d
from .Within import Within

class GappyInterp(object):
	def __init__(self,x,y,MaxGap=0.1):
		
		self.x = x
		self.y = y
		self.MaxGap = MaxGap
		
		self._CreateInterpObj()
		
		self._ListGaps()
		
	def _CreateInterpObj(self):
		
		
		self.good = np.isfinite(self.y)
		use = np.where(self.good)[0]
				
		self.fInterp = interp1d(self.x[use],self.y[use],bounds_error=False,fill_value=np.nan)


	def _ListGaps(self):
		
		use = np.where(self.good)[0]
		xu = self.x[use]
		dx = xu[1:] - xu[:-1]
		
		bad = np.where(dx > self.MaxGap)[0]
		if bad.size > 0:
			self.i0 = use[bad]
			self.i1 = use[bad+1]
			self.x0 = self.x[self.i0]
			self.x1 = self.x[self.i1]
		else:
			self.i0 = np.array([])
			self.i1 = np.array([])
			self.x0 = np.array([])
			self.x1 = np.array([])
		
		self.nGap = bad.size


	def Interp(self,x):
		
		y = self.fInterp(x)
		
		bad = self._ListBad(x)
		if bad.size > 0:
			y[bad] = np.nan
		
		return y
		
	def _ListBad(self,x):
		
		bad = []
		for i in range(0,x.size):
			for j in range(0,self.nGap):
				if Within(x[i],self.x0[j],self.x1[j]):
					bad.append(i)
						
		return np.array(bad)
