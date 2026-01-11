from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/healthcheck")
async def get_healthcheck() -> JSONResponse:
    return JSONResponse(content={"status": "OK"})
