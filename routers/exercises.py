from fastapi import APIRouter,Depends,Query
from typing import Annotated, Literal
from models import User,Exercise
from dependencies import get_session
from db_helper import create_object
from sqlmodel import  Session,select,col
from pydantic import BaseModel,Field

router = APIRouter(
    prefix="/exercises",
    tags=["exercises"],
    dependencies=[Depends(get_session)]
)


class FilterExerciseParams(BaseModel):
   id: int 
   name: str
   category: str 
   muscle_group : str 


@router.post("/")
def create_exercise(*, session: Session = Depends(get_session),exercise:Exercise):
    return create_object(session,Exercise,exercise)



@router.get("/")
def list_exercises(*, session: Session = Depends(get_session),name=None,category=None,muscle_group=None):
    statement = select(Exercise)
    if name:
        statement = statement.where(col(Exercise.name).contains(name))
    
    if category:
        statement = statement.where(Exercise.category==category)
    
    if muscle_group:
        statement= statement.where(Exercise.muscle_group==muscle_group)
    
    results = session.exec(statement).all()
    return results
