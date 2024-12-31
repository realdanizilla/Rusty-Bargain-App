# This file contains the validation schemas for the CRUD operations

from pydantic import BaseModel, PositiveFloat, EmailStr, validator, Field
from enum import Enum
from datetime import datetime
from typing import Optional

# Categorical classes as Enum
class GearboxBase(Enum):
    gearbox0 = None
    gearbox1 = "manual"
    gearbox2 = "auto"
    gearbox3 = "semi-automatic"

class FueltypeBase(Enum):
    fueltype0 = None
    fueltype1 = "gasoline"
    fueltype2 = "diesel"
    fueltype3 = "electric"
    fueltype4 = "hybrid"
    fueltype5 = "petrol"
    fueltype6 = "other"
    fueltype7 = "lpg"
    fueltype8 = "cng"

class VehicleTypeBase(Enum):
    vehicletype0 = None
    vehicletype1 = "bus"
    vehicletype2 = "convertible"
    vehicletype3 = "coupe"
    vehicletype4 = "other"
    vehicletype5 = "sedan"
    vehicletype6 = "small"
    vehicletype7 = "suv"
    vehicletype8 = "wagon"


# VehicleBase
class VehicleBase(BaseModel):
    datecrawled: Optional[datetime]
    price: Optional[int]
    vehicletype: Optional[str]
    gearbox: Optional[str]
    power: Optional[int]
    model: Optional[str]
    mileage: Optional[int]
    registrationmonth: Optional[int]
    registrationyear: Optional[int]
    fueltype: Optional[str]
    brand: Optional[str]
    notrepaired: Optional[str]
    datecreated: Optional[datetime]
    numberofpictures: Optional[int]
    postalcode: Optional[int]
    lastseen: Optional[datetime]

    @validator("gearbox")
    def check_gearbox(cls, v):
        if v in [item.value for item in GearboxBase]:
            return v
        raise ValueError("Invalid Gearbox selection")
    
    @validator("fueltype")
    def check_fueltype(cls, v):
        if v in [item.value for item in FueltypeBase]:
            return v
        raise ValueError("Invalid fuel type selection")

    @validator("vehicletype")
    def check_vehicle(cls, v):
        if v in [item.value for item in VehicleTypeBase]:
            return v
        raise ValueError("Invalid vehicle type selection")

# VehicleCreate
class VehicleCreate(VehicleBase):
    pass

# VehicleResponse
class VehicleResponse(VehicleBase):
    id: int

    class Config:
        orm_mode = True

# VehicleUpdate
class VehicleUpdate(BaseModel):
    datecrawled: Optional[datetime] = None
    price: Optional[PositiveFloat] = None
    vehicletype: Optional[str] = None
    gearbox: Optional[str] = None
    power: Optional[int] = None
    model: Optional[str] = None
    mileage: Optional[int] = None
    registrationmonth: Optional[int] = None
    registrationyear: Optional[int] = None
    fueltype: Optional[str] = None
    brand: Optional[str] = None
    repaired: Optional[bool] = None
    datecreated: Optional[datetime] = None
    numberofpictures: Optional[int] = None
    postalcode: Optional[int] = None
    lastseen: Optional[datetime] = None

    @validator("gearbox", pre=True, always=True)
    def check_gearbox(cls, v):
        if v is None:
            return v
        if v in [item.value for item in GearboxBase]:
            return v
        raise ValueError("Invalid Gearbox selection")

    @validator("fueltype", pre=True, always=True)
    def check_fueltype(cls, v):
        if v is None:
            return v
        if v in [item.value for item in FueltypeBase]:
            return v
        raise ValueError("Invalid fuel type selection")

    @validator("vehicletype", pre=True, always=True)
    def check_vehicletype(cls, v):
        if v is None:
            return v
        if v in [item.value for item in VehicleTypeBase]:
            return v
        raise ValueError("Invalid vehicle type selection")
    
class InputData(BaseModel):
    datecrawled: Optional[datetime] = None
    vehicletype:Optional[str] = None
    gearbox: Optional[str] = None
    power: Optional[int] = None
    model: Optional[str] = None
    mileage: Optional[int] = None
    registrationmonth: Optional[int] = None
    registrationyear: Optional[int] = None
    fueltype: Optional[str] = None
    brand: Optional[str] = None
    notrepaired: Optional[str] = None
    datecreated: Optional[datetime] = None
    numberofpictures: Optional[int] = None
    postalcode: Optional[int] = None
    lastseen: Optional[datetime] = None