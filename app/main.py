from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from pathlib import Path
from .database import SessionLocal
from .models import ScoreIn, Score, ScoreOut
from sqlalchemy.orm import Session
from typing import List

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
    global count
    row = Score(name=score.name, score=count)
    db.add(row)
    db.commit()
    db.refresh(row)

    count = 0
    return {"id": row.id, "name": row.name, "score": row.score, "count": count}

@app.get("/api/scores", response_model=List[ScoreOut])
async def get_scores(db: Session = Depends(get_db)):
    return db.query(Score).order_by(Score.score.desc()).all()