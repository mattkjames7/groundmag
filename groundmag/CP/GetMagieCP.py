import numpy as np
from ..ReadMagie import ReadMagie
from .CrossPhase import CrossPhase


def GetMagieCP(Date,estn,pstn,**kwargs):


	edata = ReadMagie(estn,Date)
	pdata = ReadMagie(pstn,Date)

	return CrossPhase(edata,pdata,**kwargs)