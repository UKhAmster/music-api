from pydantic import BaseModel
from typing import List, Optional


class TrackOut(BaseModel):
    title: str
    album: Optional[str]
    audio_url: str
    description_url: str
    artist_name: str

    class Config:
        from_attributes = True


class ArtistOut(BaseModel):
    id: int
    name: str
    description_url: str
    photo_url: Optional[str]

    class Config:
        from_attributes = True


class SearchResult(BaseModel):
    tracks: List[TrackOut]
    artists: List[ArtistOut]

    class Config:
        from_attributes = True

# Для подробного артиста
class TrackOnly(BaseModel):
    title: str
    album: Optional[str]
    audio_url: str
    description_url: str

    class Config:
        from_attributes = True


class ArtistDetail(BaseModel):
    name: str
    description_url: str
    photo_url: Optional[str]
    tracks: List[TrackOnly]

    class Config:
        from_attributes = True
