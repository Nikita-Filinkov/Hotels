from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.hotels.router import hotels_on_location

router = APIRouter(
    prefix='/pages',
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory='app/templates')


@router.get('/hotels')
async def get_hotels_page(
        request: Request,
        free_hotels=Depends(hotels_on_location)
):
    return templates.TemplateResponse(name='hotels.html', context={"request": request, 'free_hotels': free_hotels})
