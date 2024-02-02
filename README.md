# groundmag
A small package designed for reading ground magnetometer data.

## Installation

This package should be built as a wheel or source package.

Firstly, clone and enter the cloned directory:

```bash
git clone git@github.com:mattkjames7/groundmag.git
cd groundmag
```

To build as a wheel:

```bash
python3 setup.py bdist_wheel
pip3 install dist/groundmag-0.0.2-py3-none-any.whl
```

Or as source package:
```bash
python3 setup.py sdist
pip3 install dist/groundmag-0.0.2.tar.gz
```

Finally, set the `$GROUNDMAG_DATA` environment variable, either in your 
`~/.bashrc` file or a script you run before running python, e.g.:
```bash
export GROUNDMAG_DATA=/path/to/mag/data
```
The directory structure should be such that the path which `$GROUNDMAG_DATA`
points to should contain folders for each year of data.

## Usage

### Station information

To find out the full name and coordinates of a station:
```python
import groundmag as gm

info = gm.GetStationInfo("han")
```

### Data availability

Use `GetDataAvailability()` function to find the availability of a station, 
e.g.:

```python
import groundmag as gm

# get an array of dates
dates = gm.GetDataAvailability("han")

# plot availability for a number of stations
gm.PlotDataAvailability(["han","tar","pel","muo"],[20010101,20021231])
```

### Reading data for a single station

Use the `GetData()` function, which returns a `numpy.recarray` instance with 
the fields:
 - `Date`: integer date in the format `yyyymmdd`
 - `ut`: time in hours
 - `Bx`: x/h-component of the magnetic field
 - `By`: y/d-component of the magnetic field
 - `Bz`: z-component of the magnetic field
 - `Bm`: magnitude of the magnetic field
where HDZ vectors are returned by default.
e.g.
```python
import groundmag as gm

# a single date
data = gm.GetData("han",20200101)

#a range (from 20200101-12:00 to 20200104-23:00)
data = gm.GetData("han",[20200101,20200104],ut=[12.0,23.0])

#XYZ coords
data = gm.GetData("han",20200101,coords="xyz")

#filtering between high and low cutoff periods in seconds
data = gm.GetData("han",20200101,high=300,low=20)
```

