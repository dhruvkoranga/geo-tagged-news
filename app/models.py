from pydantic import BaseModel
from typing import List, Optional

class Keyword(BaseModel):
    id: int
    value: str
    active: bool = True

class GeoLocation(BaseModel):
    name: str
    latitude: float
    longitude: float
    address: Optional[str]


class Article(BaseModel):
    id: int
    title: str
    text: str
    locations: List[GeoLocation]

