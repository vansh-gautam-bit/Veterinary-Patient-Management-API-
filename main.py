from fastapi import FastAPI , HTTPException , Request
from fastapi.responses import JSONResponse
from database import Base , engine
from routers.pets import router as pet_router
from routers.visits import router as visit_router
from routers.owners import router as owner_router
from routers.users import router as user_router
import time

Base.metadata.create_all(bind=engine)

app=FastAPI(
    title = "Veterinary Patient Management API"
)

app.include_router(pet_router)
app.include_router(visit_router)
app.include_router(owner_router)
app.include_router(user_router)

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

@app.middleware("http")
async def log_requests(request, call_next):

    start_time = time.time()
    response = await call_next(request)
    response_time = time.time() - start_time

    print(f"Request: {request.method} |"
          f"{request.url.path} |"
          f"{response.status_code} |"
          f"{response_time:.4f} sec|"

          )
    
    return response
