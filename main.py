import base64
from pydantic import BaseModel
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
router = APIRouter()

class MinifyPayload(BaseModel):
    url: str

cache = {"txminf.net": "https://www.google.com"}

def log_info(request: Request):
    pass

@router.get("/ping")
def ping(request: Request):
    log_info(request)
    return JSONResponse(content={"result": "pong"}, headers={"Content-Type": "application/json"})

@router.post("/minify_url")
async def minify_url(payload: MinifyPayload):
    print(f"payload: {str(payload)}")
    url = payload.url
    try:
        encoded_string = base64.b64encode(url.encode('utf-8')).decode('utf-8')
        cache[url] = encoded_string
        return Response(status_code=200)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})



@router.get("/{full_path:path}")
def resolve_minified_url(request: Request, full_path: str):
    log_info(request)
    cached_value = cache.get(full_path)
    return Response(status_code=301, headers={'Location': cached_value})


app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(router)