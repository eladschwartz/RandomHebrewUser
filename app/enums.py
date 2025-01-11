
from enum import Enum

class Gender(str,Enum):
    MALE = 'זכר'
    FEMALE = 'נקבה'
    
class Environment(str,Enum):
    DEVELOPMENT = 'development'
    PRODUCTION = 'production'
    
