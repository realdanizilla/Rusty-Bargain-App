# this file is a controller for the CRUD operations of the database

from sqlalchemy.orm import Session
from crud.schemas import VehicleCreate, VehicleUpdate
from crud.models import VehicleModel


# Create function
## Create a record for a new vehicle
def create_vehicle(db: Session, vehicle: VehicleCreate):
    """Creates a new vehicle on the database

    Args:
        db (Session): Database connection session
        vehicle (VehicleCreate): Vehicle data matching the VehicleCreate schema

    Returns:
        _type_: Created Vehicle
    """
    db_vehicle = VehicleModel(**vehicle.model_dump())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


# Read functions
## retrieves a specific vehicle from the database
def get_vehicle(db: Session, vehicle_id: int):
    """Reads a vehicle from the database

    Args:
        db (Session): Database connection session
        vehicle_id (int): The id of the vehicle to be retrieved

    Returns:
        _type_: Selected vehicle with the given id
    """
    return db.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()

## retrieves all vehicles from the database
def get_vehicles(db: Session, skip: int = 0, limit: int = 100):
    """Reads all vehicles on the database

    Args:
        db (Session): Database connection session
        skip (int, optional): Pagination setup parameter. Defaults to 0.
        limit (int, optional): limits number of vehicles per page. Defaults to 100.

    Returns:
        _type_: the full list of vehicles in the database
    """
    return db.query(VehicleModel).offset(skip).limit(limit).all()


# Update function
## Update a vehicle in the database
def update_vehicle(db: Session, vehicle_id: int, vehicle: VehicleUpdate):
    """Updates information of a vehicle in the database

    Args:
        db (Session): Database connection session
        vehicle_id (int): The id of the vehicle to be updated
        vehicle (VehicleUpdate): Vehicle data matching the VehicleUpdate schema

    Returns:
        _type_: Updated vehicle information
    """
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
    return db_vehicle


# Delete function
## Delete a vehicle from the database
def delete_vehicle(db: Session, vehicle_id: int):
    """Removes a vehicle from the database

    Args:
        db (Session): Database connection session
        vehicle_id (int): The id of the vehicle to be deleted

    Returns:
        _type_: Deleted vehicle
    """
    db_vehicle = db.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()
    db.delete(db_vehicle)
    db.commit()
    return db_vehicle
