from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import APIKeyHeader
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
# Local imports
from models.user import User
from services.user_service import UserService
from services.scraper_service import CarScraper
from schemas.car import CarDataRequest, CarDataResponse, CarDataDTO
from services.auth_dependencies import get_current_user, require_role
from db.deps import get_db
from services.car_service import CarService
from configs.logger_config import setup_logger

# =======================
# Logging Configuration
# =======================
logger = setup_logger("autoblur.api")

api_key_scheme = APIKeyHeader(name="Authorization")

app = FastAPI()
logger.info("FastAPI app initialized.")

# =======================
# Exception Handlers
# =======================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

from schemas.user import RegisterRequest, LoginRequest
        
# =======================
# Endpoints
# =======================
@app.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    logger.info(f"/register endpoint called for username={request.username}")
    result = UserService.register_user(request, db)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    logger.info(f"/login endpoint called for username={request.username}")
    result = UserService.login_user(request, db)
    if result.get("error"):
        raise HTTPException(status_code=401, detail=result["error"])
    return result

@app.post("/car-data", response_model=CarDataResponse)
def get_car_data(
    request: CarDataRequest,
    token: str = Depends(api_key_scheme),
    db: Session = Depends(get_db)
):
    logger.info(f"/car-data endpoint called with token={token}")
    scraper = CarScraper()
    car_data = scraper.scrape(request.url)
    CarService.save_car(car_data.model_dump(exclude={"Images"}), db)
    return car_data