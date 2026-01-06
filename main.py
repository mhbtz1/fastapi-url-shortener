import base64
import re
from pydantic import BaseModel
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
router = APIRouter()

class MinifyPayload(BaseModel):
    url: str

cache = {}
rev_cache = {}

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
        encoded_url = f"https://{encoded_string}.co"
        
        cache[encoded_string] = url
        rev_cache[url] = encoded_url

        print(f"cache contents: {cache}")
        return JSONResponse(status_code=200, content={"url": encoded_url})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/{full_path:path}")
def resolve_minified_url(request: Request, full_path: str):
    log_info(request)
    print(f"full_path: {full_path}")
    groups = re.search(r'https://([0-9a-zA-Z=]+).co', full_path)
    print(f"groups: {groups}")
    try:
        fgroup = groups.group(1)
        print(f"fgroup: {fgroup}")
        print(f"local cache contents: {cache}")
        cached_value = cache.get(fgroup)
        return Response(status_code=301, headers={'Location': cached_value})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


app.add_middleware(CORSMiddleware, allow_credentials=True, allow_origins=["http://localhost:3000"], allow_methods=["*"], allow_headers=["*"])
app.include_router(router)