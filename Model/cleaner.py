'''
This script file clean the weather data and combine with energy data
'''
# required libraries
import pandas as pd 
import numpy as np 
import os 
import csv

def clean_file_weather(file):
    if not os.path.isfile(file):
        print("File does not exit")
        return None 
    else:
        columns = ["Max_temp","Min_temp","Dewpoint","Humidity","Max_windspeed","Min_windspeed","Max_pressure","Min_pressure","Precipitation"]
        df = pd.read_csv(file)
        # consider time, temp max, temp min, dew avg, avg humid, wind max, wind min, pressure max, pressure min, precipitation
        df = df.drop(["Time","Avgtemp","Maxdew","Mindew","Maxhumid","Minhumid","Avgwind","Avgpressure"],axis=1)
        # check leap year, and insert 29.02 row
        if df.shape[0] == 365:
            zeros = np.zeros((df.shape[1],))
            df = df.values
            df = np.insert(df,(31+28)*9,zeros).reshape(366,9)
            # convert back to DataFrame
            df = pd.DataFrame(df,columns=columns)
        else:
            df.columns = columns
        return df

def merge_files_weather(file_list,file_name):
    columns = ["Max_temp_[F]","Min_temp_[F]","Dewpoint_[F]","Humidity_[%]","Max_windspeed_[mph]","Min_windspeed_[mph]","Max_pressure_[in]","Min_pressure_[in]","Precipitation_[in]"]
    # create temp list to hold all values of dfs
    df = np.zeros((366,9))
    for file in file_list:
         _temp = clean_file_weather(file).values
         #sum up
         df += _temp
    # take average for 4 years
    df /= 4.0
    # take care 29.02
    df[31+28] *= 4.0
    # convert to df
    df = pd.DataFrame(df,columns=columns)
    # add time
    
    dates = pd.date_range("20040101",periods = 366)
    df["Time"] = dates
    # rearrange columns order
    
    columns = df.columns.to_list()
    columns = columns[-1:] + columns[:-1]
    df = df[columns]
    # write file
    df.to_csv(r"".join(file_name), index = True, header = True)
    # return 
    return df

def create_file_list(loc):
    """
    create file location for reading functions 
    """
    file_list = os.listdir(loc)
    for i in range(len(file_list)):
        file_list[i] = loc + "/" + file_list[i]
    return file_list

def clean_file_energy(file):
    """
    Get all electricity of a building
    Sum the total in 1 hour
    """
    if not os.path.isfile(file):
        #log("File does not exit")
        return None 
    
    df = pd.read_csv(file)
    # consider time, total and avg electricity consumption
    columns = ["Time","Total_Electricity_KW"]
    df = pd.read_csv(file)
    length = df.shape[0]
    # save datetime and add after computation
    dates = df["Date/Time"].values.reshape(length,1)
    # drop datetime and gas consumption
    drop_cols = [0,7,8,9,10]
    df = df.drop(df.columns[drop_cols],axis=1)
    df = df.values
    # take sum and of electricity consumption
    sum_df = np.sum(df,axis=1)
    sum_df = np.array(sum_df).reshape(length,1)
    # convert back to DataFrame
    df = np.append(dates,sum_df,1)
    df = pd.DataFrame(df,columns=columns)
    return df

def sum_day_energy(df):
    """
    Calculate the sum of the day 
    """
    if df.empty:
        return None

    columns = ["Total_Electricity_KW"]
    df = df.drop(["Time"],axis=1).values
    # sum 24 values for 1 day
    df = df.reshape((365,-1))
    df = np.sum(df,axis=1)
    # convert back to dataframe
    df = pd.DataFrame(df,columns = columns)
    # add time back
    dates = pd.date_range("20040101",periods = 366,freq='D')
    # drop 29.02
    dates = dates.drop(dates[31+28])
    df["Time"] = dates
    # rearrange columns order  
    columns = df.columns.to_list()
    columns = columns[-1:] + columns[:-1]
    df = df[columns]
    return df 

def merge_file_energy(file_list,file_name):
    """
    Merge all file in folder energy
    Add column average energy consumption
    Convert KW to MW
    """
    
    length = len(file_list)
    columns = ["Total_Electricity_[MW]"]
    # create temp list to hold all values of dfs
    df = np.zeros((365,1))
    for f in file_list:
          _temp = clean_file_energy(f)
          _temp = sum_day_energy(_temp)
          _temp = _temp.drop(["Time"],axis=1).values
          print(_temp.shape)
          #sum up
          df = df + _temp
    # convert KW to MW
    df = df / 1000.0
    # take average for the whole list
    avg = df / length
    # convert to df
    df = pd.DataFrame(df,columns = columns)
    # add avg energy 
    df["Avg_Electricity_[MW]"] = avg
    # add time back
    dates = pd.date_range("20040101",periods = 366,freq='D')
    # drop 29.02
    dates = dates.drop(dates[31+28])
    df["Time"] = dates
    # rearrange columns order
    columns = df.columns.to_list()
    columns = columns[-1:] + columns[:-1]
    df = df[columns]
    # write file
    df.to_csv(r"".join(file_name), index = True, header = True)
    # return 
    return df


def merge_wea_ener(weather_file, energy_file, file_name):
    # check file available
    if not os.path.isfile(weather_file) or not os.path.isfile(energy_file):
        print("Files do not exist")
        return None
    # open files
    weather_df = pd.read_csv(weather_file)
    energy_df = pd.read_csv(energy_file)
    # resolve the 29.02

    # merge files
    return 