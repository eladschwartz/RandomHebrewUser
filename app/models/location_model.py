from sqlalchemy import Column, Integer, String
from .base import Base, get_random_record, get_record_by_id


class Location(Base):
    __tablename__ = 'locations'
    
    id = Column(Integer, primary_key=True)
    city = Column(String(100))
    street_name = Column(String(100))
    street_number = Column(Integer)
    postal_code = Column(Integer)
    latitude = Column(String(100))
    longitude = Column(String(100))
    
    
async def get_random_location() -> Location:
    return await get_random_record(Location)


async def get_location_by_id(id: int) -> Location:
    return await get_record_by_id(id,Location)