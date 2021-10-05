# Downloading Magnetometer Data

## 1. CARISMA/CANOPUS

These data are downloaded from http://data.carisma.ca/ and http://www.carisma.ca/carisma-data-repository .

The first of those two links can be downloaded automatically using ```DownloadCarisma.py``` - it's slow, but at least it will sort itself. This only works for data beyond 20131201.

The rest of the data must be downloaded using the second link. This method involves manually selecting dates and downloading one month at a time. It tends to be a bit dodgy, especially once it goes from 5 s data to 1 s data. Not sure why, but it tends to be slightly more reliable if you download less days at a time. Check the downloaded archives for missing files!

## 2. IMAGE

There are two datasets which I have downloaded here:

The strange monthly IAGA formatted files can be downloaded using `wget` (I love you IMAGE) - this is automated using the ```DownloadIAGA()``` function from ```DownloadIMAGE.py```  - these data are 60/20/10 s resolution.

Subsets of the IMAGE array provide their own 1 s data. Some of these require contacting PIs, some of them have impenetrable websites, but FMI have a nice HTTP interface which can be automated: https://space.fmi.fi/image/plasmon/ - download this using ```DownloadStation()``` or ```DownloadAll()```.

## 3. INTERMAGNET

 So much data... all downloadable via ftp://ftp.seismo.nrcan.gc.ca/intermagnet/ using FileZilla (or whatever).

It contains some 1 s data, but mostly 60 s data (I think).

## 4. SuperMAG

I have not tapped into this one yet, but there appears to be an API...