from fastapi import FastAPI, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Artist, Track
from schemas import SearchResult, TrackOut, ArtistOut, ArtistDetail, TrackOnly

app = FastAPI(debug=True)


# Подключение к БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/search", response_model=SearchResult)
def search_music(query: str, db: Session = Depends(get_db)):
    print("🔍 /search запущен с query:", query)
    try:
        query_like = f"%{query}%"
        print("🔍 Поиск треков и артистов...")

        tracks = db.query(Track).outerjoin(Artist).filter(
            Track.title.ilike(query_like) | Artist.name.ilike(query_like)
        ).all()
        print(f"✅ Найдено треков: {len(tracks)}")

        artists = db.query(Artist).filter(
            Artist.name.ilike(query_like)
        ).all()
        print(f"✅ Найдено артистов: {len(artists)}")

        tracks_out = []
        for track in tracks:
            if not track.artist:
                print(f"⚠️ Трек без артиста: {track.title}")
                continue
            tracks_out.append(TrackOut(
                title=track.title,
                album=track.album,
                audio_url=track.audio_url,
                description_url=track.description_url,
                artist_name=track.artist.name
            ))

        artists_out = [
            ArtistOut(
                id=artist.id,
                name=artist.name,
                description_url=artist.description_url,
                photo_url=artist.photo_url
            ) for artist in artists
        ]

        print("✅ Ответ готов")
        return SearchResult(tracks=tracks_out, artists=artists_out)

    except Exception as e:
        print("❌ Ошибка в /search:", e)
        raise HTTPException(status_code=500, detail=str(e))




@app.get("/artists/id/{artist_id}", response_model=ArtistDetail)
def get_artist_by_id(artist_id: int = Path(...), db: Session = Depends(get_db)):
    try:
        artist = db.query(Artist).filter(Artist.id == artist_id).first()
        if artist is None:
            raise HTTPException(status_code=404, detail="Artist not found")

        tracks = db.query(Track).filter(Track.artist_id == artist.id).all()

        return ArtistDetail(
            name=artist.name,
            description_url=artist.description_url,
            photo_url=artist.photo_url,
            tracks=[
                TrackOnly(
                    title=track.title,
                    album=track.album,
                    audio_url=track.audio_url,
                    description_url=track.description_url
                ) for track in tracks
            ]
        )

    except Exception as e:
        print("❌ Ошибка в /artists/id/{artist_id}:", e)
        raise HTTPException(status_code=500, detail=str(e))
