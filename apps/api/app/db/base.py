from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from app.models.region import Region
from app.models.citizen_request import CitizenRequest