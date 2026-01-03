from fastapi import FastAPI, Depends, HTTPException, status, Request
from configs.cors_config import setup_cors
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel
# Local imports
from models.user import User
from models.car_image import CarImage
from services.user_service import UserService
from services.scraper_service import CarScraper
from schemas.car import CarDataRequest, CarDataResponse, CarDataDTO
from pydantic import BaseModel
from typing import List, Dict

class CarProcessResponse(BaseModel):
    car_id: int
    car: Dict
    image_ids: List[int]
from services.auth_dependencies import get_current_user, require_role
from db.deps import get_db
from services.car_service import CarService
from configs.logger_config import setup_logger

# =======================
# Logging Configuration
# =======================
logger = setup_logger("autoblur.api")

app = FastAPI()

# =======================
# CORS Middleware
# =======================
setup_cors(app)

logger.info("FastAPI app initialized.")

# =======================
# Exception Handlers
# =======================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

from schemas.user import RegisterRequest, LoginRequest
        
from sqlalchemy import select

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

@app.post("/car-data", response_model=CarProcessResponse)
def get_car_data(
    request: CarDataRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"/car-data endpoint called by user={current_user.username}")
    result = CarService.process_car_workflow(request.url, db)
    return result

@app.get("/car-image/{image_id}")
def get_car_image(
    image_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"/car-image/{image_id} endpoint called by user={current_user.username}")
    image_bytes = CarService.get_image_bytes_by_id(image_id, db)
    if image_bytes is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return Response(content=image_bytes, media_type="image/jpeg")
