from sqlalchemy import Column, Integer, Date
from .base import Base, get_random_record, get_record_by_id


class DateOfBirth(Base):
    __tablename__ = 'dob'
    
    id = Column(Integer, primary_key=True)
    date_of_birth = Column(Date, nullable=False)
    age = Column(Integer)
    
    
async def get_random_dob() -> DateOfBirth:
    return await get_random_record(DateOfBirth)

async def get_dob_by_id(id: int) -> DateOfBirth:
    return await get_record_by_id(id,DateOfBirth)