load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" 

begin

 cmap = (/ (/255.,255.,255./),(/  0.,  0.,  0./),\
           (/255.,255.,255./),(/ 29.,  0.,255./),(/126.,229., 91./),\
\;           (/ 78.,204., 67./),(/ 46.,178., 57./),(/ 30.,153., 61./),\
           (/ 46.,178., 57./),(/ 30.,153., 61./),\
           (/255.,255.,102./),(/255.,204.,102./),(/255.,136., 76./),\
           (/255., 25., 25./),(/204., 61., 61./),(/165., 49., 49./),\
           (/237.,  0.,237./),(/137.,103.,205./) /)/255.

 type  = "x11"

 YYYY  = "2020"

; array = new((/2920,40,75/),float)
 array = new((/2928,40,75/),float)
 array = 0

 jfs   = -1
 do imm = 1 , 12

  MM   = sprinti("%2.2i",imm)
  diri = "/home/disk/eos10/wycheng/LightningMachineLearning/data/WWLLN/AEfiles/"+YYYY+"/"+MM+"/"
  fils = systemfunc("ls " + diri + "*.loc")
  nfs  = dimsizes(fils)
  do ifs = 0 , nfs-1
;  do ifs = 0 , 0

   jfs = jfs + 1 
   filename = fils(ifs)
   print(""+filename)
   lines    = asciiread(filename,-1,"string")
   delim    = ":,"
;   x0       = str_get_field(lines,0,delim)
;   x1       = str_get_field(lines,1,delim)
;   x2       = str_get_field(lines,2,delim)
;   x3       = str_get_field(lines,3,delim)
;   x4       = str_get_field(lines,4,delim)
;   x5       = str_get_field(lines,5,delim)
;   x6       = str_get_field(lines,6,delim)
;   x7       = str_get_field(lines,7,delim)
;   print("x0="+x0+", x1="+x1+", x2="+x2+", x3="+x3+", x4="+x4+", x5="+x5+", x6="+x6+", x7="+x7)

   hh       = tointeger(str_get_field(lines,2,delim))
   lat      = tointeger(floor(tofloat(str_get_field(lines,5,delim))))
   lon      = tointeger(floor(tofloat(str_get_field(lines,6,delim))))

   mfs   = dimsizes(hh)
   do kfs = 0 , mfs-1
    if (abs(lat(kfs)).gt.90 .or. abs(lon(kfs)).gt.180) then
     continue
    end if

    ihh  = jfs*24 + hh(kfs)
    ilat = (lat(kfs) + 90)%180
    ilon = (lon(kfs) + 180)%360
    jhh  = tointeger(floor(ihh/3))

;    print("hh="+hh(kfs)+", lat="+lat(kfs)+", lon="+lon(kfs))
;    print("jhh="+jhh+", ilat="+ilat+", ilon="+ilon)

    if ( (ilat.ge.110) .and. (ilat.lt.150) ) then
     if ( (ilon.ge.45) .and. (ilon.lt.120) ) then
      array(jhh,ilat-110,ilon-45) = array(jhh,ilat-110,ilon-45) + 1
     end if
    end if

   end do
   delete(lines)
   delete(hh)
   delete(lat)
   delete(lon)
  end do

  delete(fils)
 end do

; t = ispan(0,8759,3)
 t = ispan(0,8783,3)
 t@units = "hours since "+YYYY+"-01-01 00:00:00"

 latitude   = fspan(20.5,59.5,40)
 latitude@units = "degrees_north"

 longitude  = fspan(-134.5,-60.5,75)
 longitude@units = "degrees_east"

 system ("rm WWLLN_"+YYYY+"_F_cg_1deg3hr_US.nc")
 setfileoption("nc","Format","LargeFile")
 ncdf = addfile("WWLLN_"+YYYY+"_F_cg_1deg3hr_US.nc" ,"c");

 fatt               = True            ; assign file attributes
 fatt@title         = "level 1 analysis"
; fatt@source_file   = ""
 fatt@Conventions   = "None"
 fatt@creation_date = systemfunc ("date")
 fileattdef( ncdf, fatt )            ; copy file attributes

 array!0    = "Time"
 array!1    = "lat"
 array!2    = "lon"

 array&Time = t
 array&lat  = latitude
 array&lon  = longitude

 array@long_name = "3-hourly Lightning Occurrence"

 ncdf->F    = array
 
end
