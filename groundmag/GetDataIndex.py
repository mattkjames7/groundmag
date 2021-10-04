import numpy as np
from . import Globals
from .ReadDataIndex import ReadDataIndex

def GetDataIndex():
	
	if Globals.DataIndex is None:
		Globals.DataIndex = ReadDataIndex()
		
	return Globals.DataIndex
