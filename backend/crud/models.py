from sqlalchemy import Column, Float, String, Integer, DateTime
from database.database import Base

# This file contains the table models for the database
# Need to review data types based on what is on the preprocessed data
class VehicleModel(Base):
    __tablename__ = "bronze_car_data"
    id = Column(Integer, primary_key=True, index=True)
    datecrawled = (Column(DateTime))
    price = Column(Integer)
    vehicletype = Column(String)
    gearbox = Column(String)
    power = Column(Integer)
    model = Column(String)
    mileage = Column(Integer)
    registrationmonth = Column(Integer) 
    registrationyear = Column(Integer)
    fueltype = Column(String)
    brand = Column(String)
    notrepaired = Column(String)
    datecreated = Column(DateTime)
    numberofpictures = Column(Integer)
    postalcode = Column(Integer)
    lastseen = Column(DateTime)