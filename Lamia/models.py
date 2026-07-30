from sqlalchemy import Column, Integer, Float, String
from database import Base

class SOSReport(Base):
    __tablename__ = "sos_reports"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(String)
    status = Column(String, default="ACTIVE")