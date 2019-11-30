import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import glob, os
from os import path 

g = 9.8
R = 6.37122e8 #in cm
mw_CH4 = 16 # g/mol
mw_air = 29 # g/mol

def airkg():
	os.chdir("/gpfsm/dnb02/projects/p54/users/imitevsk/eesc_6926_final_project/")	
	x1 = xr.open_dataset('/gpfsm/dnb02/projects/p54/users/imitevsk/eesc_6926_final_project/data/GFDL-AM4p1.tracer_level.01.nc')	
	x = [	'data/GFDL-AM4p1.tracer_level.01.nc', 'data/GFDL-AM4p1.tracer_level.02.nc', 'data/GFDL-AM4p1.tracer_level.03.nc',
			'data/GFDL-AM4p1.tracer_level.04.nc', 'data/GFDL-AM4p1.tracer_level.05.nc', 'data/GFDL-AM4p1.tracer_level.06.nc',
			'data/GFDL-AM4p1.tracer_level.07.nc', 'data/GFDL-AM4p1.tracer_level.08.nc', 'data/GFDL-AM4p1.tracer_level.09.nc',
			'data/GFDL-AM4p1.tracer_level.10.nc', 'data/GFDL-AM4p1.tracer_level.11.nc', 'data/GFDL-AM4p1.tracer_level.12.nc' ]		
	
	months = np.arange(1,13,1)
	p_coords = x1.OH.pfull
	lat_coords = x1.OH.lat
	lon_coords = x1.OH.lon

	airkg = xr.DataArray(np.zeros((len(x), p_coords.size, lat_coords.size, lon_coords.size)), [('month', months), ('pfull',p_coords), ('lat',lat_coords), ('lon',lon_coords) ], attrs={'air mass':'kg'}, name = 'airkg')
	
	#calculate area of latitude band	
	lat = np.zeros(x1.OH.lat.size +2)
	lat[1:-1] = np.array(x1.OH.lat)
	lat[0] = -90; lat[-1] = 90
	lat_sin = np.sin(np.deg2rad(lat))
	area = np.zeros(x1.OH.lat.size)
	area[:] = 2 * np.pi * R**2 * (lat_sin[2:] - lat_sin[:-2])/2
	p1 = 0
	p2 = 0
	#calculate airmass volume of box	
	for m, x_var in enumerate(x):
		X = xr.open_dataset(x_var)
		bk = X.bk
		ps = X.ps
		pk = X.pk
		print('m =',m)
		for j in range(lat_coords.size):
			#print('m =',m,'lat =',np.array(lat_coords[j]))
			#for i in range(lon_coords.size):
			for l in range(p_coords.size):
				p1 = np.array(bk[l+1]*ps[0,j,:] + pk[l+1])
				p2 = bk[l] * ps[0,j,:] + pk[l]
				airkg[m,l,j,:] = abs(p1-p2) * area[j] * 1e-4 / g
		
	DS = airkg.to_dataset(name = 'airkg')
	DS.to_netcdf("OH_airkg.nc")
	return DS


def OH_gfdl_fields():
	os.chdir("/gpfsm/dnb02/projects/p54/users/imitevsk/eesc_6926_final_project/")	
	x1 = xr.open_dataset('/gpfsm/dnb02/projects/p54/users/imitevsk/eesc_6926_final_project/data/GFDL-AM4p1.tracer_level.01.nc')	
	airkg = xr.open_dataset('/gpfsm/dnb02/projects/p54/users/imitevsk/eesc_6926_final_project/OH_airkg.nc').airkg
	x = [	'data/GFDL-AM4p1.tracer_level.01.nc', 'data/GFDL-AM4p1.tracer_level.02.nc', 'data/GFDL-AM4p1.tracer_level.03.nc',
			'data/GFDL-AM4p1.tracer_level.04.nc', 'data/GFDL-AM4p1.tracer_level.05.nc', 'data/GFDL-AM4p1.tracer_level.06.nc',
			'data/GFDL-AM4p1.tracer_level.07.nc', 'data/GFDL-AM4p1.tracer_level.08.nc', 'data/GFDL-AM4p1.tracer_level.09.nc',
			'data/GFDL-AM4p1.tracer_level.10.nc', 'data/GFDL-AM4p1.tracer_level.11.nc', 'data/GFDL-AM4p1.tracer_level.12.nc' ]		
	
	months = np.arange(1,13,1)
	p_coords = x1.OH.pfull
	lat_coords = x1.OH.lat
	lon_coords = x1.OH.lon
	
	OH = xr.DataArray(np.zeros((12, p_coords.size, lat_coords.size, lon_coords.size)), [('month', months), ('p',p_coords), ('lat',lat_coords), ('lon',lon_coords) ], attrs={'description':'OH concentration', 'units':'Tg/month','model':'GFDL'}, name = 'OH')
	
	#seconds = np.array([31,28,31,30,31,30,31,31,30,31,30,31]) * 24 * 60 * 60
	seconds = 30 * 24 * 60 * 60 #rev 1

	for m, x_var in enumerate(x):
		print('m =',m)
		X = xr.open_dataset(x_var)
		OH[m,:,:,:] = X.OH[0,:,:,:].squeeze() * (mw_CH4 / mw_air) * airkg[m,:,:,:] * 1e3 * 1e-12 * seconds 
	
	DS = OH.to_dataset(name = 'OH')
	DS.to_netcdf("OH_concentration.nc")

	DS1 = OH.mean('lon').to_dataset(name = 'OH')
	DS1.to_netcdf("OH_concentration_zonal_mean.nc")

#airkg()
OH_gfdl_fields()
