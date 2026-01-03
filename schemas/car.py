from pydantic import BaseModel


class CarDataDTO(BaseModel):
    Car_External_ID: str | None
    Car_Name: str
    Type: str
    Generation: str
    Year: str
    Mileage: str
    Fuel_Type: str
    Vehicle_Number: str
    Price: float | None

    @classmethod
    def from_scraped(cls, scraped: dict):
        return cls(
            Car_External_ID=scraped.get("Car External ID"),
            Car_Name=scraped.get("Car Name"),
            Type=scraped.get("Type"),
            Generation=scraped.get("Generation"),
            Year=scraped.get("Year"),
            Mileage=scraped.get("Mileage"),
            Fuel_Type=scraped.get("Fuel Type"),
            Vehicle_Number=scraped.get("Vehicle Number"),
            Price=scraped.get("Price"),
        )


class CarDataRequest(BaseModel):
    url: str


class CarDataResponse(BaseModel):
    Car_External_ID: str | None
    Car_Name: str
    Type: str
    Generation: str
    Year: str
    Mileage: str
    Fuel_Type: str
    Vehicle_Number: str
    Price: float | None
    Images: list[str]
