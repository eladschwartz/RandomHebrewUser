from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from .config import settings
from .routers.routers import ROUTERS
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from .enums import Environment

app = FastAPI()

# Add trusted host middleware first
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "randomhebrewuser.xyz",
        "www.randomhebrewuser.xyz",
        "randomhebrewuser-618cd838a33f.herokuapp.com" 
        "localhost",  
        "127.0.0.1"  
    ]
)

if settings.ENVIRONMENT != Environment.DEVELOPMENT:
    limiter = Limiter(key_func=get_remote_address, default_limits=["5/minute"])
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["Content-Type"],
)

if settings.ENVIRONMENT != Environment.DEVELOPMENT:
    app.add_middleware(HTTPSRedirectMiddleware)


for router in ROUTERS:
    app.include_router(router)