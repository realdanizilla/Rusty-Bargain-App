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
from database.database import engine
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from crud.schemas import InputData
from preprocessing import pipeline_dataset, pipeline_single
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



def preprocess_data()-> pd.DataFrame:
    try:
        query = 'SELECT * FROM bronze_car_data'
        data_df = pd.read_sql(query,engine)
        processed_df = pipeline_dataset.fit_transform(data_df)
        logger.info("Raw data preprocessed")
        return processed_df
    except Exception as e:
        logger.error("Raw data could not be preprocessed, error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
        
## creates the table on the database (not needed?)
# def create_table():
#     Base.metadata.create_all(engine)
#     logger.info("gold_car_data Table succesfully created!")

## loads the preprocessed dataset into the database table
def load_preprocessed_vehicle_dataset_into_database(df: pd.DataFrame):
    try:
        df.to_sql('gold_car_data', con=engine, if_exists='replace', index=False)
        logger.info("Preprocessed data loaded into gold_car_data table!")
    except:
        logger.error("Preprocessed data could not be loaded, error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
        

## trains the model and creates a pkl file
def train_model_and_create_file()-> pd.DataFrame:
    try:
        training_query = 'SELECT * FROM gold_car_data'
        data = pd.read_sql(training_query,engine)
        X = data.drop(columns=["price"])
        y = data["price"]
        X_train,  X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
        model = CatBoostRegressor(depth=7, iterations=50, l2_leaf_reg=0.1, learning_rate=0.5)
        model.fit(X_train, y_train)
        prediction = model.predict(X_test)
        mse = np.sqrt(mean_squared_error(y_test, prediction))
        print(f"model MSE: {mse}")
        joblib.dump(model, "model.pkl")
        logger.info("Model trained and model.pkl file created!")
    except Exception as e:
        logger.error("Model could not be trained, error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
        


## loads the model from the pkl file
def load_model():
    try:
        global model
        model = joblib.load("model.pkl")
        logger.info("Model loaded from model.pkl file!")
    except Exception as e:
        logger.error("Model could not be loaded, error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
        

## creates a prediction for the price
def predict_price(data:List[InputData])-> Dict[str, List]:
    if model is None:
        logger.error("Model is 'None', error: {e}")
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
        d.notrepaired,
        d.datecreated,
        d.numberofpictures,
        d.postalcode,
        d.lastseen] for d in data]

    columns = [
        "datecrawled", "vehicletype", "gearbox", "power", "model", 
        "mileage", "registrationmonth", "registrationyear", "fueltype", 
        "brand", "notrepaired", "datecreated", "numberofpictures", 
        "postalcode", "lastseen"
    ]
    try:
        df = pd.DataFrame(input_data, columns=columns)
        datetime_columns = ["datecrawled", "datecreated", "lastseen"]
        #for col in datetime_columns:
        #    if col in df.columns:
        #        df[col] = df[col].astype(str).replace("NaT", None) 
        processed_single_df = pipeline_single.fit_transform(df)
        logger.info("Submitted data ran through preprocessing pipeline")
        expected_feature_order = model.feature_names_
        missing_columns = set(expected_feature_order) - set(processed_single_df.columns)
        # Add missing columns and fill with 0
        for col in missing_columns:
            processed_single_df[col] = 0
        processed_single_df = processed_single_df[expected_feature_order]
        prediction = model.predict(processed_single_df)
        logger.info("Prediction has been generated!")
    except Exception as e:
        logger.error("Prediction could not be generated, error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    return {"Price prediction": prediction.tolist()}