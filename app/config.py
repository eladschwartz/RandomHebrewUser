from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str
    
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    origin_dev: str
    origins_prod: str
    
    class Config:
        env_file=".env"
    
    @property
    def origins(self) -> str:
        return self.origin_dev if self.ENVIRONMENT == "development" else self.origins_prod
        
    
    
settings = Settings()


