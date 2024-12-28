# This file handles the ETL process for the data and main functions
# It also handles raw data preprocessing and loading into the database

import os
import time
import requests
import logging
import logfire
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from logging import basicConfig, getLogger
from database.database import Base, VehicleDatabase, Session, engine
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from crud.schemas import InputData
from preprocessing import pipeline
from typing import List, Dict
from fastapi import HTTPException

# ------------------------------------------------------
# Logfire setup
logfire.configure()
basicConfig(handlers=[logfire.LogfireLoggingHandler()])
logger = getLogger(__name__)
logger.setLevel(logging.INFO)
logfire.instrument_requests()
logfire.instrument_sqlalchemy()
# ------------------------------------------------------

# Functions below are used to start from raw data and end with a trained model file
## loads the initial dataset into a dataframe and preprocess it

filepath = 'data/car_data.csv'

def preprocess_data(df: pd.DataFrame)-> pd.DataFrame:
    processed_df = pipeline.fit_transform(df)
    return processed_df
    
## creates the table on the database
def create_table():
    Base.metadata.create_all(engine)
    logger.info("Table succesfully created!")

## loads the preprocessed dataset into the database table
def load_preprocessed_vehicle_dataset_into_database(path):
    pass

## trains the model and creates a pkl file
def train_model_and_create_file(dataset):
    data = dataset
    X = data.drop(columns=["price"])
    y = data["price"]
    X_train,  X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    model = CatBoostRegressor(depth=7, iterations=50, l2_leaf_reg=0.1, learning_rate=0.5)
    model.fit(X_train, y_train)
    prediction = model.predict(X_test)
    mse = np.sqrt(mean_squared_error(y_test, prediction))
    joblib.dump(model, "model.pkl")


## loads the model from the pkl file
def load_model():
    global model
    model = joblib.load("model.pkl")
    return {"Message": "Model loaded"}

## creates a prediction for the price
def predict_price(data:List[InputData])-> Dict[str, List]:
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    input_data = [[
        d.datecrawled,
        d.vehicletype,
        d.gearbox,
        d.power,
        d.model,
        d.mileage,
        d.registrationmonth,
        d.registrationyear,
        d.fueltype,
        d.brand,
        d.repaired,
        d.datecreated,
        d.numberofpictures,
        d.postalcode,
        d.lastseen] for d in data]
    try:
        prediction = model.predict(input_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"Price prediction": prediction.tolist()}