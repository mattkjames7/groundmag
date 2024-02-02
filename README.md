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


