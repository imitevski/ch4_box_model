import xarray as xr 
import numpy as np 
import pandas as pd

def wetland():
	x1 = xr.open_dataset('WetCHARTs_extended_ensemble.nc4', decode_times = False)
	x1 = x1.wetland_CH4_emissions
		
	time = pd.date_range(start = '1/2001', end = '1/2016', freq = '1M')
	LAT = x1.lat
	
	x_wet = xr.DataArray(np.zeros((time.size, LAT.size)), [('time', time), ('lat',LAT) ], attrs={'description':'Zonal mean Wetland Emission averaged over 18 models',"units" : "g / month", "dataset_doi" : "doi.org/10.3334/ORNLDAAC/1502"}, name = 'wetland_emissions')
		
	R = 6.37122e6 #in m	

	#calculate area of latitude band	
	lat = np.zeros(x1.lat.size +2)
	lat[1:-1] = np.array(x1.lat)
	lat[0] = -90; lat[-1] = 90
	lat_sin = np.sin(np.deg2rad(lat))
	area = np.zeros(x1.lat.size)
	area[:] = 2 * np.pi * R**2 * (lat_sin[2:] - lat_sin[:-2])/2

	x_wet[:,:] = np.array(x1.mean(dim=['model','lon']))	
	for i in range(time.size):
		x_wet[i,:] = x_wet[i,:] * area.transpose() * 30 * 1e-3
		
	DS = x_wet.to_dataset(name = 'wetland_emissions')
	DS.to_netcdf("wetland_emissions_zonal_model_mean.nc")
	return DS

def ch4_antropogenic():
	x1 = xr.open_dataset('CH4-em-anthro_input4MIPs_emissions_CMIP_CEDS-2017-05-18_gn_197001-201412.nc').CH4_em_anthro
	
	time = pd.date_range(start = '1/1970', end = '1/2015', freq = '1M')
	LAT = x1.lat
	
	x_ch4 = xr.DataArray(np.zeros((time.size, LAT.size)), [('time', time), ('lat',LAT) ], attrs={'description':'Zonal mean CH4 Antropogenic Emissions averaged over 8 sectors',"units" : "g / month", "tracking id" : "hdl:21.14100/92f20329-752c-4f8d-8ecc-693562803c81"}, name = 'ch4_antro')
	
	R = 6.37122e6 #in m	

	#calculate area of latitude band	
	lat = np.zeros(x1.lat.size +2)
	lat[1:-1] = np.array(x1.lat)
	lat[0] = -90; lat[-1] = 90
	lat_sin = np.sin(np.deg2rad(lat))
	area = np.zeros(x1.lat.size)
	area[:] = 2 * np.pi * R**2 * (lat_sin[2:] - lat_sin[:-2])/2

	x_ch4[:,:] = np.array(x1.mean(dim=['sector','lon']))	
	for i in range(time.size):
		x_ch4[i,:] = x_ch4[i,:] * area.transpose() * 30 * 1e3
		
	DS = x_ch4.to_dataset(name = 'ch4_antro')
	DS.to_netcdf("ch4_antropogenic_emissions_zonal_model_mean.nc")
	return DS

	
#wetland()
ch4_antropogenic()
