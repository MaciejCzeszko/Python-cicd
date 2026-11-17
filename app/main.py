from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI()

count = 0

PAGE = (Path(__file__).parent / "templates" / "index.html").read_text(encoding="utf-8")


@app.get("/", response_class=HTMLResponse)
async def index():
    return PAGE.replace("__COUNT__", str(count))


@app.post("/api/click")
async def click():
    global count
    count += 1
    return {"count": count}
