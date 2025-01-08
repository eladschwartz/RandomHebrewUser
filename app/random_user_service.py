from typing import Dict, Any
import logging
from pydantic import ValidationError
from .models import user_model, phone_model, date_of_birth_model, location_model
from . import schemas

USER = 'user'
PHONE = 'phone'
DOB = 'dob'
LOCATION = 'location'
SEED = 'seed'

class RandomUserServiceException(Exception):
    pass

class MissingRequiredFieldError(RandomUserServiceException):
    pass

class InvalidDataError(RandomUserServiceException):
    pass

class RandomUserService:
    REQUIRED_FIELDS = {
        USER: user_model.User,
        PHONE: phone_model.PhoneNumber,
        DOB: date_of_birth_model.DateOfBirth,
        LOCATION: location_model.Location
    }

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def create_random_user(self, **kwargs) -> schemas.RandomUser:
        try:
            self._validate_input(kwargs)
            
            model_user: user_model.User = kwargs[USER]
            model_phone: phone_model.PhoneNumber = kwargs[PHONE]
            model_dob: date_of_birth_model.DateOfBirth = kwargs[DOB]
            model_location: location_model.Location = kwargs[LOCATION]
            seed = kwargs[SEED]
            
            name = self._create_name(model_user)
            dob = self._create_dob(model_dob)
            location = self._create_location(model_location)
            
            random_user = schemas.RandomUser(
                name=name,
                email=model_user.email,
                gender=model_user.gender,
                phone=model_phone.phone_number,
                dob=dob,
                location=location,
                seed=seed
             )
            
            self._logger.info(f"Successfully created RandomUser: {name.first_name} {name.last_name}")
            return random_user
            
        except (MissingRequiredFieldError, InvalidDataError) as e:
            self._logger.error(str(e))
            raise
        except Exception as e:
            self._logger.error(f"Unexpected error in create_random_user: {str(e)}")
            raise RandomUserServiceException(f"Failed to create random user: {str(e)}") from e


    def _validate_input(self, kwargs: Dict[str, Any]) -> None:
        missing_fields = [field for field in self.REQUIRED_FIELDS if field not in kwargs]
        if missing_fields:
            raise MissingRequiredFieldError(f"Missing required fields: {', '.join(missing_fields)}")
        
        for field_name, expected_type in self.REQUIRED_FIELDS.items():
            value = kwargs.get(field_name)
            if not isinstance(value, expected_type):
                raise InvalidDataError(
                    f"Invalid type for {field_name}. Expected {expected_type.__name__}, "
                    f"got {type(value).__name__}"
                )

    def _create_name(self, model_user: user_model.User) -> schemas.Name:
        try:
            return schemas.Name(
                first_name=model_user.first_name,
                last_name=model_user.last_name,
                gender=model_user.gender,
                title=model_user.title
            )
        except ValidationError as e:
            raise InvalidDataError(f"Invalid name data: {str(e)}")

    def _create_dob(self, model_dob: date_of_birth_model.DateOfBirth) -> schemas.DateOfBirth:
        try:
            return schemas.DateOfBirth(
                date_of_birth=model_dob.date_of_birth,
                age=model_dob.age
            )
        except ValidationError as e:
            raise InvalidDataError(f"Invalid date of birth data: {str(e)}")

    def _create_street(self, model_location: location_model.Location) -> schemas.Street:
        try:
            return schemas.Street(
                number=model_location.street_number,
                name=model_location.street_name
            )
        except ValidationError as e:
            raise InvalidDataError(f"Invalid street data: {str(e)}")

    def _create_coordinates(self, model_location: location_model.Location) -> schemas.Coordinate:
        try:
            return schemas.Coordinate(
                latitude=model_location.latitude,
                longitude=model_location.longitude
            )
        except ValidationError as e:
            raise InvalidDataError(f"Invalid coordinate data: {str(e)}")

    def _create_location(self, model_location: location_model.Location) -> schemas.Location:
        try:
            street = self._create_street(model_location)
            coordinates = self._create_coordinates(model_location)
            
            return schemas.Location(
                street=street,
                city=model_location.city,
                postcode=model_location.postal_code,
                coordinates=coordinates
            )
        except ValidationError as e:
            raise InvalidDataError(f"Invalid location data: {str(e)}")