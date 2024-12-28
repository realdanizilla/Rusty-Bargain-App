from sqlalchemy import Column, Float, String, Integer, DateTime, Bool
from database.database import Base

# This file contains the table models for the database
# Need to review data types based on what is on the preprocessed data
class VehicleModel(Base):
    __tablename__ = "gold_car_data"
    id = Column(Integer, primary_key=True, auto_increment=True)
    datecrawled = (Column(DateTime))
    price = Column(Float, nullable=False)
    vehicletype = Column(String(30), nullable=False)
    gearbox = Column(String(10), nullable=False)
    power = Column(Integer, nullable=False)
    model = Column(String(20), nullable=False)
    mileage = Column(Integer, nullable=False)
    registrationmonth = Column(Integer, nullable=False) 
    registrationyear = Column(Integer, nullable=False)
    fueltype = Column(String(20), nullable=False)
    brand = Column(String(30),nullable=False)
    repaired = Column(Bool, nullable=False )
    datecreated = Column(DateTime, nullable=False)
    numberofpictures = Column(Integer, nullable=False)
    postalcode = Column(Integer, nullable=False)
    lastseen = Column(DateTime, nullable=False)