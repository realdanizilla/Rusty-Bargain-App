import joblib
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
    return {"message": "Welcome to the Car Price Prediction API"}

# CRUD operations for the vehicle table
## Create a new vehicle
@router.post("/vehicles/", response_model=VehicleResponse)
def create_vehicle_endpoint(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    return create_vehicle(db, vehicle)


## Retrieve all vehicles
@router.get("/vehicles/", response_model=List[VehicleResponse])
def read_vehicles_endpoint(db: Session = Depends(get_db)):
    vehicles = get_vehicles(db)
    return vehicles

## Retrieve a specific vehicle
@router.get("/vehicles/{vehicle_id}", response_model=VehicleResponse)
def read_vehicle_endpoint(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = get_vehicle(db, vehicle_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle

## Update a vehicle
@router.put("/vehicles/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle_endpoint(
    vehicle_id: int, vehicle: VehicleUpdate, db: Session = Depends(get_db)
):
    db_vehicle = update_vehicle(db, vehicle_id=vehicle_id, vehicle=vehicle)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle

## Delete a vehicle
@router.delete("/vehicles/{vehicle_id}", response_model=VehicleResponse)
def delete_vehicle_endpoint(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = delete_vehicle(db, vehicle_id=vehicle_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle


# ML endpoints
## Preprocess raw data
@router.get("/preprocessdata/")
def preprocess_data_endpoint():
    preprocess_data()
    return {'Message': 'Data preprocessed'}

@router.get("/load_preprocessed_dataset")
def load_preprocessed_data_endpoint(df):
    load_preprocessed_vehicle_dataset_into_database(df)
    return {'Message': 'Preprocessed data loaded into database'}

## Train the model
@router.get("/train_model/")
def train_model_endpoint():
    train_model_and_create_file()
    return {'Message': 'Model trained'}

## Load the model
@router.get("/load_model/")
def load_model_endpoint():
    load_model()
    return {'Message': 'Model loaded'}


## Predict the price
@router.post("/predict_price/")
def predict_price_endpoint(data:List[InputData]):
    predict_price(data)
    return {'Message: Price predicted'}
