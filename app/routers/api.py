from typing import Annotated
from fastapi import  APIRouter, Query, HTTPException, status
from ..models import user_model, phone_model, date_of_birth_model, location_model, seed_model
from .. import schemas
from ..random_user_service import RandomUserService
import asyncio
import uuid

router = APIRouter(
     prefix="/api",
     tags = ['API']
)


async def get_data_by_seed(seed: str):
    try:
         seed_record = await seed_model.get_user_by_seed(seed)
         if not seed_record:
            return None
        
         if seed_record:
            tasks = [
                user_model.get_user_by_id(seed_record.user_id),
                phone_model.get_phone_by_id(seed_record.phone_id),
                date_of_birth_model.get_dob_by_id(seed_record.dob_id),
                location_model.get_location_by_id(seed_record.location_id)
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, Exception):
                    raise result
                
            user, phone, dob, location = results
            return user, phone, dob, location, seed_record.seed

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve data: {str(e)}"
        )
            
       
async def create_random_data(filter_query: Annotated[schemas.FilterParams, Query()]):
        tasks = [
            user_model.get_random_user(filter_query.gender),
            phone_model.get_random_phone(),
            date_of_birth_model.get_random_dob(),
            location_model.get_random_location()
        ]

        user, phone, dob, location = await asyncio.gather(*tasks)

        seed = filter_query.seed or str(uuid.uuid4())
        await seed_model.create_user_seed(
            seed=seed,
            user_id=user.id,
            phone_id=phone.id,
            dob_id=dob.id,
            location_id=location.id
        )
        
        return user, phone, dob, location, seed

@router.get("/")
async def get_data(filter_query: Annotated[schemas.FilterParams, Query()]):
    try:
        if filter_query.seed:
            result = await get_data_by_seed(filter_query.seed)
            
            #if we have seed in db, just get the data
            if result:
                    user, phone, dob, location, seed = result
            #if that seed provided not in db, create one, save it in db, then return a user with that seed
            else:
                    result = await create_random_data(filter_query)
                    user, phone, dob, location, seed = result
                    
        #user didn't send 'seed' as query param, create seed and return the user with that seed
        else:
            result = await create_random_data(filter_query)
            user, phone, dob, location, seed = result
        
        service = RandomUserService()
        user = service.create_random_user(
            user=user,
            phone=phone,
            dob=dob,
            location=location,
            seed=seed
        )
    except Exception as e:
          raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate random user: {str(e)}"
        )
    
    return user
  
    


