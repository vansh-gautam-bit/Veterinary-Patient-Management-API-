from fastapi import FastAPI , HTTPException , Request
from fastapi.responses import JSONResponse
from database import Base , engine
from routers.pets import router as pet_router
from routers.visits import router as visit_router
from routers.owners import router as owner_router

Base.metadata.create_all(bind=engine)

app=FastAPI(
    title = "Veterinary Patient Management API"
)

app.include_router(pet_router)
app.include_router(visit_router)
app.include_router(owner_router)

@app.get("/",tags = ["Json Page"])
def root():
    return {
        "message": "Veterinary Patient Management API is running"
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(
    request:Request,
    exc: HTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success":False,
            "message": exc.detail
        }
    )
