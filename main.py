import base64
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
router = APIRouter()
cache = {"txminf.net": "https://www.google.com"}

def log_info(request: Request):
    pass

@router.get("/ping")
def ping():
    return JSONResponse(content={"result": "pong"}, headers={"Content-Type": "application/json"})

@router.post("/minify_url/{url}")
def minify_url(request: Request, url: str):



@router.get("/{full_path:path}")
def resolve_minified_url(request: Request, full_path: str):
    log_info(request)
    cached_value = cache.get(full_path)
    return Response(status_code=301, headers={'Location': cached_value})


app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(router)