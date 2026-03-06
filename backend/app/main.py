import os
from dotenv import load_dotenv
import yaml

from fastapi import FastAPI, Body, Depends, Header, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# from starlette.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select, text
from datetime import datetime, timezone

from .db import Base, engine, get_db
from .models import Task
from .schemas import TaskCreate, TaskUpdate, TaskOut


load_dotenv()  # Load environment variables from .env file if present

API_KEY = os.environ.get("API_KEY", "devsecops-demo-secret-CHANGEME")


app = FastAPI(title="Task Manager API", version="1.0.0")


class CacheStaticFiles(StaticFiles):
    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)
        # Cache 1 jour pour les fichiers statiques
        if response.status_code == 200:
            response.headers["Cache-Control"] = "public, max-age=86400"
        return response


# Monter les fichiers statiques seulement si demandé et si le dossier existe
if os.environ.get("SERVE_FRONTEND_STATIC", "0") == "1":
    frontend_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../frontend")
    )
    if os.path.isdir(frontend_path):
        app.mount("/static", CacheStaticFiles(directory=frontend_path), name="static")


@app.get("/")
def serve_frontend():
    index_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../frontend/index.html")
    )
    if os.path.exists(index_path):
        return FileResponse(index_path, media_type="text/html")
    return {"message": "Frontend not found. Please build or add index.html."}


# Allow local frontend (file:// or http://localhost) during training
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get("/debug")
def debug(x_api_key: str | None = Header(default=None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"env": dict(os.environ)}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/admin/stats")
def admin_stats(x_api_key: str | None = Header(default=None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"tasks": "…"}


@app.post("/import")
def import_yaml(payload: str = Body(embed=True)):
    try:
        data = yaml.safe_load(payload)
    except yaml.YAMLError as e:
        raise HTTPException(status_code=400, detail=f"YAML error: {e}")
    return {
        "imported": True,
        "keys": list(data.keys()) if isinstance(data, dict) else "n/a",
    }


@app.get("/tasks", response_model=list[TaskOut])
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.execute(select(Task).order_by(Task.id.desc())).scalars().all()
    return tasks


@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = Task(
        title=payload.title.strip(), description=payload.description, status="TODO"
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.get("/tasks/search", response_model=list[TaskOut])
def search_tasks(q: str = Query(""), db: Session = Depends(get_db)):
    like_query = f"%{q}%"
    sql = text("SELECT * FROM tasks WHERE title LIKE :q OR description LIKE :q")
    rows = db.execute(sql, {"q": like_query}).mappings().all()
    return [Task(**r) for r in rows]


@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if payload.title is not None:
        task.title = payload.title.strip()
    if payload.description is not None:
        task.description = payload.description
    if payload.status is not None:
        task.status = payload.status

    task.updated_at = datetime.now(timezone.utc)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return None
