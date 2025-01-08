from fastapi import  APIRouter
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter(
     prefix="",
     tags = ['']
)



@router.get("/")
async def home():
    #The website template, if needed one.
    pass
