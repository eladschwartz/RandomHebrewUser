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
    origin_dev: str = "http://127.0.0.1:8000" 
    origins_prod: str
    
    class Config:
        env_file=".env"
    
    @property
    def origins(self) -> list[str]:
        if self.ENVIRONMENT == "development":
            return [self.origin_dev]
        else:
            return [origin.strip() for origin in self.origins_prod.split(",")]
        
    
    
settings = Settings()


