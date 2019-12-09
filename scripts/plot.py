import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 

def CH4_emissions_seasonal():
	x_extended = xr.open_dataset('data/WetCHARTs_extended_ensemble.nc4', decode_times = False) 
	
	x_extended['time'] = pd.date_range('2001-01-01', periods=x_extended.time.size, freq='MS')
	time = x_extended.time + (x_extended.time.diff(dim='time', label='lower')/2)
	x_extended.time.values[:-1] = time
	x_extended.time.values[-1] = np.datetime64('2015-12-16T12:00:00.000000000')
	
	fig = plt.figure()
	fig.set_figwidth(fig.get_figwidth() * 3) 
	fig.set_figheight(fig.get_figheight() * 3)
	
	axes = fig.add_subplot(3,1,1)
	x_extended.wetland_CH4_emissions.sum(dim=['lat','lon','model']).plot(label = 'all year', color = 'black')
	x_extended.wetland_CH4_emissions.sel(lat = slice(0,90)).sum(dim=['lat','lon','model']).plot(label = 'NH', color = 'red')
	x_extended.wetland_CH4_emissions.sel(lat = slice(-90,0)).sum(dim=['lat','lon','model']).plot(label = 'SH', color = 'blue')
	plt.legend(loc=1)
	plt.xlabel('Time')
	plt.ylabel('Wetland CH$_4$ emission\n(mg m$^2$ day$^{-1}$)')
	
	axes = fig.add_subplot(3,1,2)
	x_extended.wetland_CH4_emissions.sum(dim=['lat','lon','model']).plot(label = 'all year', color = 'black')
	x_extended.wetland_CH4_emissions.sel(lat = slice(20,90)).sum(dim=['lat','lon','model']).plot(label = '20N-90N', color = 'red')
	x_extended.wetland_CH4_emissions.sel(lat = slice(-90,-20)).sum(dim=['lat','lon','model']).plot(label = '20S-90S', color = 'blue')
	x_extended.wetland_CH4_emissions.sel(lat = slice(-20,20)).sum(dim=['lat','lon','model']).plot(label = '20S-20N', color = 'green')
	plt.legend(loc=1)
	plt.ylabel('Wetland CH$_4$ emission\n(mg m$^2$ day$^{-1}$)')
	plt.xlabel('Time')
	
	axes = fig.add_subplot(3,1,3)
	x_extended.wetland_CH4_emissions.sum(dim=['lat','lon','model']).plot(label = 'all year', color = 'black')
	x_extended.wetland_CH4_emissions.sel(lat = slice(20,90)).sum(dim=['lat','lon','model']).plot(label = '20N-90N', color = 'red')
	x_extended.wetland_CH4_emissions.sel(lat = slice(-90,-20)).sum(dim=['lat','lon','model']).plot(label = '20S-90S', color = 'blue')
	x_extended.wetland_CH4_emissions.sel(lat = slice(0,20)).sum(dim=['lat','lon','model']).plot(label = '0-20N', color = 'green')
	x_extended.wetland_CH4_emissions.sel(lat = slice(-20,0)).sum(dim=['lat','lon','model']).plot(label = '20S-0', color = 'cyan')
	plt.legend(loc=1)
	plt.ylabel('Wetland CH$_4$ emission\n(mg m$^2$ day$^{-1}$)')
	plt.xlabel('Time')
	
	
	plt.tight_layout()
	plt.savefig('CH4_emissions_seasonal.pdf')
	plt.show()

def OH_gfdl_fields():
	x1 = xr.open_dataset('data/GFDL-AM4p1.tracer_level.01.nc')
	x2 = xr.open_dataset('data/GFDL-AM4p1.tracer_level.02.nc')
	x3 = xr.open_dataset('data/GFDL-AM4p1.tracer_level.03.nc')
	x4 = xr.open_dataset('data/GFDL-AM4p1.tracer_level.04.nc')
	x5 = xr.open_dataset('data/GFDL-AM4p1.tracer_level.05.nc')
	x6 = xr.open_dataset('data/GFDL-AM4p1.tracer_level.06.nc')
	x7 = xr.open_dataset('data/GFDL-AM4p1.tracer_level.07.nc')
	x8 = xr.open_dataset('data/GFDL-AM4p1.tracer_level.08.nc')
	x9 = xr.open_dataset('data/GFDL-AM4p1.tracer_level.09.nc')
	x10 = xr.open_dataset('data/GFDL-AM4p1.tracer_level.10.nc')
	x11 = xr.open_dataset('data/GFDL-AM4p1.tracer_level.11.nc')
	x12 = xr.open_dataset('data/GFDL-AM4p1.tracer_level.12.nc')
	
	y = np.array([	x1.OH.sum(), x2.OH.sum(), x3.OH.sum(), x4.OH.sum(), x5.OH.sum(), x6.OH.sum(),
					x7.OH.sum(), x8.OH.sum(), x9.OH.sum(), x10.OH.sum(), x11.OH.sum(), x12.OH.sum()])
	x = np.arange(1,13)

	fig = plt.figure()
	plt.plot(y)
	plt.xlabel('Months')
	plt.ylabel('OH concentration')
	plt.title('Monthly averaged OH field (2012-2017) from GFDL') 
	plt.tight_layout()
	plt.savefig('OH_concentration.pdf') 
	plt.show()
		
#CH4_emissions_seasonal()
OH_gfdl_fields()
