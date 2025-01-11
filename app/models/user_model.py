from sqlalchemy import Column, Integer, String, select, func
from .base import Base, get_record_by_id
import random
from ..database import AsyncSessionLocal
from ..enums import Gender

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(10))  
    first_name = Column(String(100), nullable=False)
    last_name= Column(String(100), nullable=False)
    gender = Column(String(10)) 
    email = Column(String(100), nullable=False)
    
async def get_user_by_id(id: int) -> User:
    return await get_record_by_id(id,User)

async def get_random_user(gender: str | None = None) -> User:
    async with AsyncSessionLocal() as session:
        try:
            valid_genders = {Gender.MALE, Gender.FEMALE}  
            if not isinstance(gender, str) or gender not in valid_genders:
                gender = None
                
            try:
                # First we getting the number of all users records
                query = select(func.count(User.id))
                #  if user pass gender param, use it.
                if gender is not None:
                    query = query.where(User.gender == gender)
                                        
                count = await session.execute(query)
                count = count.scalar_one()

                random_offset = random.randint(0, count - 1)
                
                query = select(User)
                if gender is not None:
                    query = query.where(User.gender == gender)
                    
                random_user = await session.execute(query.offset(random_offset).limit(1))

                return random_user.scalar_one_or_none()
            
            except Exception as e:
                print(e)
                
        finally:
            await session.close()
