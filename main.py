import string, random, validators

from fastapi                 import FastAPI, HTTPException, Depends
from fastapi.responses       import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm          import Session
from pydantic                import BaseModel
from database                import SessionLocal, URL
from datetime                import datetime, timedelta
from typing                  import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

class URLShortenRequest(BaseModel):
    url: str
    expiration_hours: Optional[int] = None
    
class URLShortenResponse(BaseModel):
    short_url: str
    expiration_hours: Optional[int] = None

class StatsResponse(BaseModel):
    short_key: str
    num_visits: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_short_url(db: Session):
    characters = string.ascii_letters + string.digits
    while True:
        short_url = ''.join(random.choices(characters, k=6))
        if not db.query(URL).filter(URL.short_key == short_url).first():
            return short_url

def is_valid_url(url: str) -> bool:
    return validators.url(url)

@app.post("/shorten/")
async def shorten_url(request: URLShortenRequest, db: Session = Depends(get_db)):
    if not is_valid_url(request.url):
        raise HTTPException(status_code=400, detail="Invalid URL format")

    existing_url = db.query(URL).filter(URL.original_url == request.url).first()

    if existing_url:
        expiration_hours = (existing_url.expiration_date - datetime.utcnow()).total_seconds() // 3600 if existing_url.expiration_date else None

        return URLShortenResponse(short_url=existing_url.short_key, expiration_hours=expiration_hours)

    short_url = generate_short_url(db)
    expiration_date = None
    
    if request.expiration_hours:
        expiration_date = datetime.utcnow() + timedelta(hours=request.expiration_hours)
    
    db_url = URL(
        short_key=short_url,
        original_url=request.url,
        expiration_date=expiration_date,
        visit_counts=0
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    
    return URLShortenResponse(short_url=short_url, expiration_hours=request.expiration_hours)

@app.get("/{short_url}")
async def redirect_to_original_url(short_url: str, db: Session = Depends(get_db)):
    db_url = db.query(URL).filter(URL.short_key == short_url).first()
    
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    if db_url.expiration_date and db_url.expiration_date < datetime.utcnow():
        db.delete(db_url)
        db.commit()
        raise HTTPException(status_code=404, detail="URL has expired")
    
    db_url.visit_counts += 1
    db.commit()
    
    return RedirectResponse(url=db_url.original_url, status_code=301)

@app.get("/stats/{short_key}")
async def get_stats(short_key: str, db: Session = Depends(get_db)):
    db_url = db.query(URL).filter(URL.short_key == short_key).first()
    
    if not db_url:
        raise HTTPException(status_code=404, detail="Short key not found")
    
    return StatsResponse(short_key=short_key, num_visits=db_url.visit_counts)