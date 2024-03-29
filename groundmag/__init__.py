from . import Globals
from ._PopulateStations import _PopulateStations

#populate the station list
if Globals.Stations is None:
	_PopulateStations()


from ._ReadBinary import _ReadBinary
from .ReadData import ReadData
from .PlotData import PlotData
from .GetStationInfo import GetStationInfo
from .PlotChain import PlotChain
from .GetData import GetData
from .Spectrum import Spectrum
from .PlotSpectrum import PlotSpectrum
from .Spectrogram import Spectrogram
from .PlotSpectrogram import PlotSpectrogram
from .PlotSpectrogramChain import PlotSpectrogramChain
from .PlotPolarization import PlotPolarization
from .PlotPolarizationChain import PlotPolarizationChain
from .xyz2hdz import xyz2hdz
from .hdz2xyz import hdz2xyz
from .DateToYear import DateToYear
from .GetDataAvailability import GetDataAvailability
from .PlotDataAvailability import PlotDataAvailability
from .SaveData import SaveData
from .Convert import ConvertDir,ConvertCanopus,ConvertCarisma1Hz,ConvertCarisma8Hz,ConvertIMAGE1Hz,ConvertIMAGEiaga,ConvertINTERMAGNET
from ._ReadBinaryFile import _ReadBinaryFile
from .ReadDataIndex import ReadDataIndex,_ReadIndexFile
from .UpdateDataIndex import UpdateDataIndex
from .GetDataIndex import GetDataIndex
from ._ReadIAGA2002 import _ReadIAGA2002
from .ListFiles import ListFiles
from .GetChain import GetLatChain,GetLonChain
from .SpecPolarization import SpecPolarization,FullSpecPolarization

from . import Trace
from . import Tools


from .ReadMagie import ReadMagie


from . import CP