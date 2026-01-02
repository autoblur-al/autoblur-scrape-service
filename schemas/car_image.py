from pydantic import BaseModel

class CarImageDTO(BaseModel):
    id: int
    path: str
    order: int
    car_id: int