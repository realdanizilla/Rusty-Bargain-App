# this file is a controller for the CRUD operations of the database

from sqlalchemy.orm import Session
from crud.schemas import VehicleCreate, VehicleUpdate
from crud.models import VehicleModel
from typing import Any
from logging_config import setup_logging

logger = setup_logging()

# Create function
## Create a record for a new vehicle
def create_vehicle(db: Session, vehicle: VehicleCreate)->dict:
    """Creates a new vehicle on the database

    Args:
        db (Session): Database connection session
        vehicle (VehicleCreate): Vehicle data matching the VehicleCreate schema

    Returns:
        new_vehicle_data: Created Vehicle information
    """
    try:
        logger.info(f"Creating entry: {vehicle}")
        db_vehicle = VehicleModel(**vehicle.model_dump())
        db.add(db_vehicle)
        db.commit()
        db.refresh(db_vehicle)
        logger.info("Entry created successfully")
        return db_vehicle
        
    except Exception as e:
        logger.error(f"Error creating entry: {e}")
        return None


# Read functions
## retrieves a specific vehicle from the database
def get_vehicle(db: Session, vehicle_id: int)->dict:
    """Reads a vehicle from the database

    Args:
        db (Session): Database connection session
        vehicle_id (int): The id of the vehicle to be retrieved

    Returns:
        vehicle_data: Information for selected vehicle with the given id
    """
    try:
        logger.info(f"Reading entry with ID: {vehicle_id}")
        query = db.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()
        logger.info("Entry read successfully")
        print(query)
        return query
    except Exception as e:
        logger.error(f"Error reading entry: {e}")
        return None
    

## retrieves all vehicles from the database
def get_vehicles(db: Session, skip: int = 0, limit: int = None)->list[dict[str,Any]]:
    """Reads all vehicles on the database

    Args:
        db (Session): Database connection session
        skip (int, optional): Pagination setup parameter. Defaults to 0.
        limit (int, optional): limits number of vehicles per page. Defaults to None.

    Returns:
        vehicles_data: the full list of dictionaries with vehicles from the database
    """
    try:
        logger.info("Reading all entries")
        query = db.query(VehicleModel).offset(skip)
        if limit is not None:
            query = query.limit(limit)
        logger.info("Entries read successfully")
        return query.all()
    except Exception as e:
        logger.error(f"Error reading entries: {e}")
        return None


# Update function
## Update a vehicle in the database
def update_vehicle(db: Session, vehicle_id: int, vehicle: VehicleUpdate)->dict:
    """Updates information of a vehicle in the database

    Args:
        db (Session): Database connection session
        vehicle_id (int): The id of the vehicle to be updated
        vehicle (VehicleUpdate): Vehicle data matching the VehicleUpdate schema

    Returns:
        updated_vehicle_data: Updated vehicle information
    """
    try:
        logger.info(f"Updating entry with ID: {vehicle_id}")
        db_vehicle = db.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()

        if db_vehicle is None:
            return None   
        if vehicle.datecrawled is not None:
            db_vehicle.datecrawled = vehicle.datecrawled
        if vehicle.price is not None:
            db_vehicle.price = vehicle.price
        if vehicle.vehicletype is not None:
            db_vehicle.vehicletype = vehicle.vehicletype 
        if vehicle.gearbox is not None:
            db_vehicle.gearbox = vehicle.gearbox
        if vehicle.power is not None:
            db_vehicle.power = vehicle.power
        if vehicle.model is not None:
            db_vehicle.model = vehicle.model
        if vehicle.mileage is not None:
            db_vehicle.mileage = vehicle.mileage
        if vehicle.registrationmonth is not None:
            db_vehicle.registrationmonth = vehicle.registrationmonth
        if vehicle.registrationyear is not None:
            db_vehicle.registrationyear = vehicle.registrationyear
        if vehicle.fueltype is not None:
            db_vehicle.fueltype = vehicle.fueltype
        if vehicle.brand is not None:
            db_vehicle.brand = vehicle.brand
        if vehicle.repaired is not None:
            db_vehicle.repaired = vehicle.repaired
        if vehicle.datecreated is not None:
            db_vehicle.datecreated = vehicle.datecreated
        if vehicle.numberofpictures is not None:
            db_vehicle.numberofpictures = vehicle.numberofpictures
        if vehicle.postalcode is not None:
            db_vehicle.postalcode = vehicle.postalcode
        if vehicle.lastseen is not None:
            db_vehicle.lastseen = vehicle.lastseen   
        db.commit()
        logger.info("Entry updated successfully")
        return db_vehicle
    except Exception as e:
        logger.error(f"Error updating entry: {e}")
        return None


# Delete function
## Delete a vehicle from the database
def delete_vehicle(db: Session, vehicle_id: int)->dict:
    """Removes a vehicle from the database

    Args:
        db (Session): Database connection session
        vehicle_id (int): The id of the vehicle to be deleted

    Returns:
        delete_vehicle_data: Information for the Deleted vehicle
    """
    try:
        logger.info(f"Deleting entry with ID: {vehicle_id}")
        db_vehicle = db.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()
        db.delete(db_vehicle)
        db.commit()
        logger.info("Entry deleted successfully")
        return db_vehicle
    except Exception as e:
        logger.error(f"Error deleting entry: {e}")
        return None
