from sqlalchemy.orm import  DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import select, func
import random
from typing import Type
from ..database import AsyncSessionLocal

class Base(AsyncAttrs, DeclarativeBase):
    pass


async def get_random_record[T:Base](model: Type[T]):
    async with AsyncSessionLocal() as session:
        try:
            query = select(func.count(model.id))
            count = await session.execute(query)
            count = count.scalar_one()

            random_offset = random.randint(0, count - 1)
                
            query = select(model)
            random_phone = await session.execute(query.offset(random_offset).limit(1))

            return random_phone.scalar_one_or_none()
        finally:
            session.close()
            
            
async def get_record_by_id[T:Base](id: int, model: Type[T]):
    async with AsyncSessionLocal() as session:
        try:
              query = select(model).where(model.id == id)
              result = await session.execute(query)
              return result.scalar_one_or_none()
        finally:
            session.close()
    
    