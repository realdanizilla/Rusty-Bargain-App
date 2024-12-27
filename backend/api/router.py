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
from ELT import load_model, train_model_and_create_file

router = APIRouter()

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


# Model training endpoints
## Train the model
@router.get("/trainmodel/")
def train_model_endpoint():
    train_model_and_create_file()

## Load the model
@router.get("/loadmodel/")
def load_model_endpoint():
    return load_model()


## Predict the price
@router.post("/predictprice/")
def predict_price_endpoint(data:List[InputData]):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
