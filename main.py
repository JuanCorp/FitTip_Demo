from fastapi import FastAPI,Depends,File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, SQLModel, create_engine, select
import models
from openai_helper import get_response_open_ai,create_baseline_prompt


from routers import users, workouts,exercises,meals,openai
from dependencies import create_db_and_tables,get_session
from db_helper import initiate_db


origins = [
    "http://localhost",
    "http://localhost:3000",
]


app = FastAPI()
app.include_router(users.router)
app.include_router(workouts.router)
app.include_router(exercises.router)
app.include_router(meals.router)
app.include_router(openai.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    create_db_and_tables()


@app.get("/initial-setup")
def initial_setup(session: Session = Depends(get_session)):
    initiate_db(session)
    return True



app.mount("/", StaticFiles(directory="static", html=True), name="static")