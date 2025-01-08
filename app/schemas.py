from pydantic import BaseModel,EmailStr
from datetime import date

    
class FilterParams(BaseModel):
    gender : str | None = None
    seed: str | None = None
 

class Coordinate(BaseModel):
    latitude: str
    longitude: str


class Street(BaseModel):
    number: int
    name: str

class Location(BaseModel):
    street: Street
    city: str 
    postcode: int
    coordinates: Coordinate
    
    
class Name(BaseModel):
    first_name: str
    last_name: str 
    title: str | None = None 

class DateOfBirth(BaseModel):
    date_of_birth: date
    age: int
    

class RandomUser(BaseModel):
    name: Name
    email: EmailStr
    gender: str
    phone: str
    dob: DateOfBirth
    location: Location
    seed: str