load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" 

begin

 YYYYs          = "2013"
 varname        = "cape"

 filename       = "/home/disk/eos10/wycheng/LightningMachineLearning/data/ERA5_v1/"+YYYYs+"/3D/ERA5_"+YYYYs+"_"+varname+".nc"

 erafile        = addfile(filename, "r")

 arrayi     = short2flt(erafile->$varname$(:,:,:))

 dim = dimsizes(arrayi)
 nfs = dim(0)
 ny  = dim(1)
 nx  = dim(2)
 mfs = nfs/3

 array = new((/nfs,ny,nx/),float)
 nxhf  = tointeger(floor(nx/2))

 tmp1 = arrayi(:,::-1,:)

 delete(arrayi)

 array(:,:,0:nxhf-1) = tmp1(:,:,nxhf:nx-1)
 array(:,:,nxhf:nx-1) = tmp1(:,:,0:nxhf-1)

 delete(tmp1)

 arrayo = new((/mfs,40,75/),float)

 do ihh = 0 , mfs-1
  print("ihh = "+ihh)
  do ilat = 110 , 150-1
   do ilon =  45 , 120-1
    arrayo(ihh,ilat-110,ilon-45) = avg(array(ihh*3:ihh*3+2,ilat*4:ilat*4+3,ilon*4:ilon*4+3))
   end do
  end do
 end do

 t = fspan(0,nfs-3,mfs)
 t@units = "hours since "+YYYYs+"-01-01 00:00:00"

 latitude   = fspan( 20.5,59.5,40)
 latitude@units = "degrees_north"

 longitude  = fspan(-134.5,-60.5,75)
 longitude@units = "degrees_east"

 system ("rm ERA5_"+YYYYs+"_"+varname+"_cg_1deg3hr.nc")
 ncdf = addfile("ERA5_"+YYYYs+"_"+varname+"_cg_1deg3hr.nc" ,"c")

 fatt               = True            ; assign file attributes
 fatt@title         = ""
; fatt@source_file   = ""
; fatt@Conventions   = "None"
 fatt@creation_date = systemfunc ("date")
 fileattdef( ncdf, fatt )            ; copy file attributes

 arrayo!0    = "Time"
 arrayo!1    = "lat"
 arrayo!2    = "lon"

 arrayo&Time = t
 arrayo&lat  = latitude
 arrayo&lon  = longitude

 ncdf->$varname$    = arrayo

end
