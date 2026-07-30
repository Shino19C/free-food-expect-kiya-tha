try:
    from pydantic import BaseModel, ConfigDict
except ImportError:
    from pydantic import BaseModel
    ConfigDict = None


class SOSCreate(BaseModel):
    device_id: str
    latitude: float
    longitude: float
    timestamp: str


class SOSResponse(SOSCreate):
    id: int
    status: str

    if ConfigDict is not None:
        model_config = ConfigDict(from_attributes=True)
    else:
        class Config:
            from_attributes = True
