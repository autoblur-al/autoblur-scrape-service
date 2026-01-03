from pydantic import BaseModel


class CarImageDTO(BaseModel):
    id: int
    path: str
    url: str
    order: int
    car_id: int
