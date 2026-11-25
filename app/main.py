import threading
from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import Score, ScoreIn, ScoreOut

app = FastAPI()

count = 0
count_lock = threading.Lock()

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
    with count_lock:
        count += 1
        return {"count": count}

@app.post("/api/save")
def save_score(score: ScoreIn, db: Session = Depends(get_db)):  # noqa: B008
    global count
    with count_lock:
        row = Score(name=score.name, score=count)
        db.add(row)
        db.commit()
        count = 0
        reset_count = count
    return {"id": row.id, "name": row.name, "score": row.score, "count": reset_count}

@app.get("/api/scores", response_model=list[ScoreOut])
def get_scores(db: Session = Depends(get_db)):  # noqa: B008
    return db.query(Score).order_by(Score.score.desc()).limit(10).all()