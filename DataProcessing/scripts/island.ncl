load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"

begin

; input

 lsfile         = addfile("$NCARG_ROOT/lib/ncarg/data/cdf/landsea.nc","r")
 lsdata         = lsfile->LSMASK

 latitude   = fspan(20.5,59.5,40)
 latitude@units = "degrees_north"

 longitude  = fspan(-134.5,-60.5,75)
 longitude@units = "degrees_east"

 isl0       = landsea_mask(lsdata,latitude,longitude)
 island     = where(isl0.eq.1 .or. isl0.eq.3,1,0)

 system ("rm island_1deg_US.nc")
 ncdf = addfile("island_1deg_US.nc" ,"c")

 fatt               = True            ; assign file attributes
 fatt@title         = ""
 fatt@source_file   = ""
 fatt@Conventions   = "None"
 fatt@creation_date = systemfunc ("date")
 fileattdef( ncdf, fatt )            ; copy file attributes

 island!0    = "lat"
 island!1    = "lon"

 island&lat  = latitude
 island&lon  = longitude

 ncdf->island = island

end

