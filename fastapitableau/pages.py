from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from fastapi.routing import APIRouter
from fastapi import Request

statics = StaticFiles(packages=["fastapitableau"])
templates = Jinja2Templates(directory="templates")

built_in_pages = APIRouter()

@built_in_pages.get("/")
async def home(request: Request):
    context = {
        "head_content": "head_content",
        "title_desc": "title_desc",
        "body_content": "body_content",
        "request": request
    }
    return templates.TemplateResponse("index.html", context=context)

@built_in_pages.get("/user_guide")
async def user_guide(request: Request):
    routes = request.app.routes
    context = {
        "title": request.app.title,
        "routes": routes,
        "request": request
    }
    return templates.TemplateResponse("user_guide.html", context=context)
