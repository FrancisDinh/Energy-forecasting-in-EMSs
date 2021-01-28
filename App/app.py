#Library
from flask import Flask
import json, codecs
import pandas as pd
import numpy as np
import tensorflow as tf
import keras
import joblib
from sklearn.preprocessing import MinMaxScaler


#global variable
api_path = "../api/"
file_path = "../Data_acquisition/Final DB/commercial/"
model_path = api_path + "model.hdf5"
scaler_path = api_path + "scaler.gz"
data_path = file_path + "merged_energy.csv"
window_size = 7

app = Flask(__name__)
@app.route("/")
def hello():
    return "Guten Tag!"

def model_forecast(model, series, window_size):
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(window_size, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(window_size))
    ds = ds.batch(32).prefetch(1)
    forecast = model.predict(ds)
    return forecast

@app.route("/forecast", methods=["GET", "POST"])
@app.route("/forecast<int:steps>", methods=["GET", "POST"])
def forecast(steps = 1):
    #if not (series or scaler_loaded or model_loaded):
    #    return "Please check code, error in path"
    #scale data
    series_scaled = scaler_loaded.transform(series.reshape(-1,1))
    #forecast
    _based_series = series_scaled
    results = []
    for i in range(steps):
        _based_series = _based_series[-window_size:]
        _r = model_forecast(model_loaded, _based_series.reshape(-1,1),window_size)[-1,-1]
        results.append(_r[0])
        _based_series = np.append(_based_series,_r)
    #convert back to normal scale
    results = np.array(results)
    results = scaler_loaded.inverse_transform(results.reshape(-1,1)).reshape(-1,).tolist()
    return json.dumps(results)
'''
@app.route("/today", method=["POST"])
def get_today():
    pass
'''

if __name__ == "__main__":
    #read data and pre-trained model
    series = pd.read_csv(data_path)["Avg_Electricity_[MW]"][-window_size:].to_numpy()
    scaler_loaded = joblib.load(scaler_path)
    model_loaded = keras.models.load_model(model_path)
    #run app
    app.run(host="0.0.0.0", port=4848,debug=True)
