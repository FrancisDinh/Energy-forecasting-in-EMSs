# Energy consumption forecasting in energy management systems
This repo contains the code for the Master Thesis of the same title. The thesis started on 07.01.2020 and ended on 04.01.2020.

There are two study cases commercial buildings and housholds. We attempted to use six RNN-based models to forecast energy consumption, then compare them with ARIMA.
To prove the feasibility of a new service, which can forecast future demand, we used the best performer in RNN-based models for building an API, only for the study case commercials buildings.

### Required libraries
- python 3
- flask
- flask_restful
- json
- nbimporter
- pickle
- joblib
- tensorflow 2.3
- keras
### Installation guide
- Get Cuda, Cudnn, python3 and virtualenv: To complete the installation, it is required to have Graphic card fron Nvdia, because the project was building on tensorflow GPU, which is compatible to Nvdia hardware.
- Create env: 
```
python3 -m venv tensorflow_env
```
- Activate: 
```
source tensorflow_env/bin/activate
```
- Install and upgrade pip
```
pip install --upgrade pip
```
- Install tensorflow 2.3 or up
```
pip install --upgrade tensorflow==version
pip install --upgrade tensorflow-gpu
```
- Install Jupyter notebook
```
pip install jupyter
```
### Components
- Data_acquisition: contains DBs and cleaner notebooks for both buildings. The weather cleaner notebook for households is not neccessary.
    - Raw DB
        - commercial
        - household
    - Final DB
        - commercial
        - household
- Model: for each study cases, there are notebooks:
    - analysis: basic analysis of the study case
    - arima: forecasting using ARIMA
    - dnn: forecasting using DNN
    - rnn: forecasting using RNN-based models
- App: contains app.py, the restful API
- api: contains the stored data of the pre-trained model

### Running guide
After finish setting up the environment, one can run:
- Activate environment
```
source tensorflow_env/bin/activate
```
- Go to folder App
```
python3 app.py
```
- The API is available for observation at: localhost, port 4848. Using command to ask model to predict:
```
/forecast<int:days>
```
- Retrain model: go to folder Model and process the notebook forecasting_model


