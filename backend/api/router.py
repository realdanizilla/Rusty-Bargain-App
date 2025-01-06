import joblib
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal, get_db
from crud.schemas import VehicleResponse, VehicleUpdate, VehicleCreate, InputData
from typing import List
from crud.controller import (
    create_vehicle,
    get_vehicle,
    get_vehicles,
    update_vehicle,
    delete_vehicle
)
from ELT import (
    load_model,
    train_model_and_create_file,
    preprocess_data,
    load_preprocessed_vehicle_dataset_into_database,
    predict_price
)

router = APIRouter()

# root endpoint
@router.get("/")
def read_root():
    """ Returns standard message to check if API is working

    Returns:
        dict: A dictionary with a message key
    """
    return {"message": "Welcome to the Car Price Prediction API"}

# CRUD operations for the vehicle table
## Create a new vehicle
@router.post("/vehicles/", response_model=VehicleResponse)
def create_vehicle_endpoint(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    """Create a new vehicle

    Args:
        vehicle (VehicleCreate): The vehicle to be created
        db (Session, optional): Database connection session. Defaults to Depends(get_db).

    Returns:
        dict: The created vehicle
    """
    return create_vehicle(db, vehicle)


## Retrieve all vehicles
@router.get("/vehicles/", response_model=List[VehicleResponse])
def read_vehicles_endpoint(db: Session = Depends(get_db)):
    """Retrieve all vehicles

    Args:
        db (Session, optional): Database connection session. Defaults to Depends(get_db).

    Returns:
        dict: A list with all vehicles
    """
    vehicles = get_vehicles(db)
    return vehicles

## Retrieve a specific vehicle
@router.get("/vehicles/{vehicle_id}", response_model=VehicleResponse)
def read_vehicle_endpoint(vehicle_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific vehicle

    Args:
        vehicle_id (int): The id of the vehicle to be retrieved
        db (Session, optional): Database connection session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the vehicle is not found

    Returns:
        dict: The selected vehicle
    """
    db_vehicle = get_vehicle(db, vehicle_id=vehicle_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle

## Update a vehicle
@router.put("/vehicles/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle_endpoint(
    vehicle_id: int, vehicle: VehicleUpdate, db: Session = Depends(get_db)
):
    """Update a vehicle

    Args:
        vehicle_id (int): The id of the vehicle to be updated
        vehicle (VehicleUpdate): The new data for the vehicle according to the VehicleUpdate schema
        db (Session, optional): Database connection session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the vehicle is not found

    Returns:
        dict: The updated vehicle
    """
    db_vehicle = update_vehicle(db, vehicle_id=vehicle_id, vehicle=vehicle)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle

## Delete a vehicle
@router.delete("/vehicles/{vehicle_id}", response_model=VehicleResponse)
def delete_vehicle_endpoint(vehicle_id: int, db: Session = Depends(get_db)):
    """Delete a vehicle

    Args:
        vehicle_id (int): The id of the vehicle to be deleted
        db (Session, optional): Database connection session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the vehicle is not found

    Returns:
        dict: The deleted vehicle
    """
    db_vehicle = delete_vehicle(db, vehicle_id=vehicle_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle



# ML endpoints

# setting up a global variable to store the processed dataframe
global_processed_dataframe = None

## Preprocess raw data
@router.get("/preprocessdata/")
def preprocess_data_endpoint():
    """Preprocess the raw data from bronze table

    Returns:
        DataFrame: The preprocessed data
    """
    global global_processed_dataframe
    global_processed_dataframe = preprocess_data()
    return {'Message': 'Data preprocessed'}

@router.get("/load_preprocessed_dataset")
def load_preprocessed_data_endpoint():
    """Load the preprocessed data into the gold table
    """
    global global_processed_dataframe
    load_preprocessed_vehicle_dataset_into_database(global_processed_dataframe)
    return {'Message': 'Preprocessed data loaded into database'}

## Train the model
@router.get("/train_model/")
def train_model_endpoint():
    """Train the model and create a pkl file
    """
    train_model_and_create_file()
    return {'Message': 'Model trained'}

## Load the model
@router.get("/load_model/")
def load_model_endpoint():
    """Load the model from the pkl file
    """
    load_model()
    return {'Message': 'Model loaded'}


## Predict the price
@router.post("/predict_price/")
def predict_price_endpoint(data:List[InputData]):
    """Predict the price of a vehicle

    Args:
        data (List[InputData]): The data to be used for the prediction according to the InputData schema

    Returns:
        dict: The predicted price
    """
    result = predict_price(data)
    return {'Message': 'Price predicted', **result}
