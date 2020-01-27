from . import Globals
from ._PopulateStations import _PopulateStations

#populate the station list
if Globals.Stations is None:
	_PopulateStations()


from ._ReadBinary import _ReadBinary
from .ReadData import ReadData
from .PlotData import PlotData
