;
;	function ReadMag,Date,Station,Res=Res
;
;	Inputs
;	======
;	Date : long
;		Date in the format yyyymmdd
;	Station : string
;		Station code
;	Res : int
;		Time resolution in seconds (not always included in the file name)
;
;	Returns
;	=======
;	out : struct
;		out.Date : long
;			Date in the format yyyymmdd.
;		out.ut :	double
;			Time of the day in hours.
;		out.Bx : double
;			X (north/south) field in nT.
;		out.By : double
;			Y (east/west) field in nT.
;		out.Bz : double
;			Z (vertical) field in nT.
;
function ReadMag,Date,Station,Res=Res

	; work out the file name
	year = Date/10000
	fpath = '/data/sol-ionosphere/gnd_mag_data/' + string(year,format='(I04)') + '/'
	fname0 = string(Date,format='(I08)') + '-' + strupcase(Station)
	if keyword_set(Res) then begin
		 fname0 = fname0 + '-' + string(Res,'(I0)') + 's'
	endif
	fname = fpath + fname0 + '.mag.gz'
	
	; check that the file exists beforehand
	if ~file_test(fname) then begin
		; file doesn't exist
		return,!NULL
	endif
	
	; copy to a temporary directory
	r = string(fix(randomu(seed,1)*100000000),format='(I08)')
	tpath = '~/tmp/' + r + '/'
	spawn,'mkdir -p ' + tpath
	spawn,'cp ' + fname + ' ' + tpath
	
	; extract	
	gzname = tpath + fname0 + '.mag.gz'
	spawn,'gunzip ' + gzname
	tname = tpath + fname0 + '.mag'
	
	; define the structure of the output
	dtype = {	Date:0L,	$
				ut:0D,		$
				Bx:0D,		$
				By:0D,		$
				Bz:0D}
	
	; read the data in
	openr,unit,tname,/get_lun
	n = 0L
	readu,unit,n
	
	out = replicate(dtype,n)
	ut = dblarr(n)
	Bx = dblarr(n)
	By = dblarr(n)
	Bz = dblarr(n)
	readu,unit,ut
	readu,unit,Bx
	readu,unit,By
	readu,unit,Bz
	free_lun,unit
	
	out.Date = Date
	out.ut = ut
	out.Bx = Bx
	out.By = By
	out.Bz = Bz

	; delete temp file
	spawn,'rm ' + tname
	spawn,'rm -d ' + tpath
	
	return,out
end
