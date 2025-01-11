from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import select
from .base import Base
from ..database import AsyncSessionLocal

class UserSeed(Base):
    __tablename__ = 'seeds'
    
    id = Column(Integer, primary_key=True)
    seed = Column(String(100), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    phone_id = Column(Integer, ForeignKey('phones.id'), nullable=False)
    dob_id = Column(Integer, ForeignKey('dob.id'), nullable=False)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)

async def get_user_by_seed(seed: str) -> UserSeed | None:
    async with AsyncSessionLocal() as session:
        try:
            query = select(UserSeed).where(UserSeed.seed == seed)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        finally:
            await session.close()

async def create_user_seed(seed: str,user_id: int,phone_id: int,dob_id: int,location_id: int) -> UserSeed:
        async with AsyncSessionLocal() as session:
            try:
                user_seed = UserSeed(
                    seed=seed,
                    user_id=user_id,
                    phone_id=phone_id,
                    dob_id=dob_id,
                    location_id=location_id
                )
                session.add(user_seed)
                await session.commit()
                await session.refresh(user_seed)
                return user_seed
            finally:
                await session.close()