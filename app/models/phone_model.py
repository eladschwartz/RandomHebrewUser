from sqlalchemy import Column, Integer, String
from .base import Base, get_random_record, get_record_by_id
from sqlalchemy.ext.asyncio import AsyncSession

class PhoneNumber(Base):
    __tablename__ = 'phones'
    
    id = Column(Integer, primary_key=True)
    phone_number = Column(String(20), nullable=False)
    

async def get_random_phone() -> PhoneNumber:
    return await get_random_record(PhoneNumber)

async def get_phone_by_id(id: int) -> PhoneNumber:
    return await get_record_by_id(id,PhoneNumber)