# This file handles the ETL process for the data and main functions
# It also handles raw data preprocessing and loading into the database

import os
import time
import requests
import logging
import logfire
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from logging import basicConfig, getLogger
from database.database import Base, VehicleDatabase, Session, engine

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
def preprocess_initial_dataset(path):
    vehicle_df = pd.read_csv(path)

## creates the table on the database
def create_table():
    Base.metadata.create_all(engine)
    logger.info("Table succesfully created!")

## loads the preprocessed dataset into the database
def load_preprocessed_vehicle_dataset_into_database(path):
    pass

## trains the model and creates a pkl file
def train_model_and_create_file():
    pass

## loads the model from the pkl file
def load_model():
    pass

## creates a prediction for the price
def predict_price():
    pass