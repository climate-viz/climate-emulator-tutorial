import xarray as xr
import numpy as np

DATA_VAR_LABELS = {
    'tas': {
        'ylabel': 'Annual Global Surface \n Temperate Anomaly in °C',
        'title': 'Surface Temperature, "tas"',
    },
    'pr': {
        'ylabel': 'Annual Mean Precipitation in mm/day',
        'title': 'Precipitation, "pr"',
    }
}
# Climatebench utilities for normalizing the input data
# Code adapted from: https://github.com/duncanwp/ClimateBench/
# blob/main/baseline_models/CNN-LTSM_model.ipynb
def normalize(data, var, meanstd):
    """
    # to-do: move to dataloader.py
    #        and use torch
    Args:
        data
        var string: dictionary key to data variable, e.g., 'CO2'
        meanstd: dictionary of means and standard deviations
            of each var. E.g., meanstd['CO2'] is a tuple of (mean, std)
    """
    mean = meanstd[var][0]
    std = meanstd[var][1]
    return (data - mean)/std

def unnormalize(data, var, meanstd):
    mean = meanstd[var][0]
    std = meanstd[var][1]
    return data * std + mean

def compute_mean_std_X_train(data_arr, var='CO2'):
    """
    Compute mean and standard deviaation across a data_arr that is list
    of xarray.DataArray for [ssp126, ssp370, ssp585, hist-aer and hist-ghg]. The
    magic numbers in the code are indices from [0,...,4] for [ssp126,..., hist-ghg].
    The data_arr is concatenated in a way that the overlapping historical periods
    are removed before calculating mean and standard deviation.
    Returns
        mean np.array(1)
        std np.array(1)
    """
    # To not take the historical data into account several time we have to slice the scenario datasets
    # and only keep the historical data once (in the first ssp index 0 in the simus list)
    len_historical = len(data_arr[3].time)
    data_arr_concat = np.concatenate(
        [data_arr[i][var].data for i in [0, # ssp126 historical + future data 
                                        3, 4]] + # modified scenarios over historical time-period
        [data_arr[i][var].sel(time=slice(len_historical, None)).data for i in 
         range(1, 3)]) # future points from ssp370, ssp585
    mean = data_arr_concat.mean()
    std = data_arr_concat.std()

    return mean, std

def normalize_data_arr(data_arr, meanstd, keys=['CO2', 'CH4', 'SO2', 'BC']):
    """ normalizes all variables in the data_arr. The data_arr is a list
    of xarray.DataArray that each can contain multiple keys. The keys
    can have varying dimensions, e.g., local or global.
    Args:
        meanstd: dictionary of means and standard deviations of each var. E.g., meanstd['CO2'] is a tuple of (mean, std)
    Returns:
        data_arr_norm 
    """
    data_arr_norm = [] 
    for i, data in enumerate(data_arr): 
        for key in keys: 
            # Get dimensions of each variable, e.g., 'time' for global variables and ['time', 'lat', 'lon'] for local variables
            dims = data[key].dims
            # Apply the normalization function across every variable via xarray's assign
            data=data.assign({key: (dims, normalize(data[key].data, key, meanstd))}) 
        data_arr_norm.append(data)
    return data_arr_norm

def load_climatebench_data(
    simus = ['ssp126','ssp370','ssp585','hist-GHG','hist-aer'],
    len_historical = 165,
    data_path = 'data/',
    avg_over_ensemble = True):
    """ Load ClimateBench Training Data
    Loads the scenario passed in <simus> from data_path into memory. 
    The data from scenarios, e.g., ssp126 is concatenated with historical 
    data.
    Args:
        avg_over_ensemble bool: If True, will return average over ensemble
            members in dataset.
    Returns:
        inputs list(xarray.Dataset[len_historical (+ len_future), lon, lat]) 
            with CO2, SO2, CH4, BC in float64
        targets list(xarray.Dataset[len_historical (+ len_future), lon, lat]) 
            with diurnal_temperature_range & tas in float32 and pr & pr90 in float64
    """
    # to-do: load only co2 and temp
    #        make possible to load rest later on
    # do lazy loading to highlight benefit of netCDF

    inputs = []
    targets = []

    for i, simu in enumerate(simus):

        input_name = 'inputs_' + simu + '.nc'
        output_name = 'outputs_' + simu + '.nc'

        if 'hist' in simu:
            # load inputs
            input_xr = xr.open_dataset(data_path + input_name)

            # load outputs
            output_xr = xr.open_dataset(data_path + output_name)

        # Concatenate with historical data in the case of scenario 'ssp126', 'ssp370' and 'ssp585'
        else:
            # load inputs
            input_paths = [data_path + 'inputs_historical.nc', # ground-truth historical data, e.g., (165,)
                           data_path + input_name] # future data, e.g., (86,)
            input_xr = xr.open_mfdataset(input_paths).compute() 

            # load outputs, taking average across ensemble members
            output_paths = [data_path + 'outputs_historical.nc',
                            data_path + output_name]
            output_xr = xr.open_mfdataset(output_paths)

        # Process precipitations
        output_xr = output_xr.assign({"pr": output_xr.pr * 86400,
                                    "pr90": output_xr.pr90 * 86400})
        output_xr = output_xr.drop(['quantile'])
        # Process dimensions
        output_xr = output_xr.rename({'lon':'longitude', 'lat': 'latitude'})
        if avg_over_ensemble:
            # Average over ensemble members
            output_xr = output_xr.mean(dim='member')
            output_xr = output_xr.transpose('time','latitude', 'longitude')
        else:
            output_xr = output_xr.transpose('member', 'time','latitude', 'longitude')
        output_xr = output_xr.compute() # load into memory

        print(input_xr.dims, simu)

        # Append to list
        inputs.append(input_xr)
        targets.append(output_xr)

    return inputs, targets
