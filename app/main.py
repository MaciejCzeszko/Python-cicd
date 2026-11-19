from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from pathlib import Path
from .database import SessionLocal
from .models import ScoreIn, Score
from sqlalchemy.orm import Session

app = FastAPI()

count = 0

PAGE = (Path(__file__).parent / "templates" / "index.html").read_text(encoding="utf-8")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def index():
    return PAGE.replace("__COUNT__", str(count))


@app.post("/api/click")
async def click():
    global count
    count += 1
    return {"count": count}

@app.post("/api/save")
def save_score(score: ScoreIn, db: Session = Depends(get_db)):
    row = Score(name=score.name, score=score.score)
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id, "name": row.name, "score": row.score}