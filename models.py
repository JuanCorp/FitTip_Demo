from typing import Annotated
import datetime 
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select,Relationship


class User(SQLModel,table=True):
    id: int | None = Field(default=None,primary_key=True)
    email: str = Field(index=True) 
    weight: float
    height: float 
    goal: str
    gender: str| None 

    workouts: list["Workout"] = Relationship(back_populates="user")
    workout_templates: list["Workout_Template"] = Relationship(back_populates="user")
    meals: list["Meal_Checklist"] = Relationship(back_populates="user")


class Workout_Template_Exercise(SQLModel,table=True):
    template_id: int | None = Field(default=None,foreign_key="workout_template.id",primary_key=True)
    exercise_id: int | None = Field(default=None,foreign_key="exercise.id",primary_key=True)
    template: "Workout_Template" = Relationship(back_populates="template_exercises")
    exercise: "Exercise" = Relationship(back_populates="template_exercises")
    
    weight: float | None 
    repetitions: float | None 
    duration: int | None 
    


class Workout_Template(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    template_exercises: list["Workout_Template_Exercise"] = Relationship(back_populates="template")
    user_id: int = Field(foreign_key="user.id")
    user: User | None = Relationship(back_populates="workout_templates")



class Workout(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    user_id: int = Field(foreign_key="user.id")
    
    user: User| None  = Relationship(back_populates="workouts")
    exercises: list["Workout_Exercise"] = Relationship(back_populates="workout")



class Exercise(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    category: str 
    muscle_group : str 
    video_url : str | None 

    template_exercises: list["Workout_Template_Exercise"] = Relationship(back_populates="exercise")
    workout_exercises: list["Workout_Exercise"] = Relationship(back_populates="exercise")



class Workout_Exercise(SQLModel,table=True):
    id: int | None  = Field(default=None,primary_key=True)
    sets : list["Workout_Exercise_Set"] = Relationship(back_populates="workout_exercise")

    workout_id : int  = Field(foreign_key="workout.id")
    workout : Workout | None = Relationship(back_populates="exercises")

    exercise_id : int = Field(foreign_key="exercise.id")
    exercise : Exercise | None = Relationship(back_populates="workout_exercises")



class Workout_Exercise_Set(SQLModel,table=True):
    id: int | None  = Field(default=None,primary_key=True)
    weight: float | None 
    repetitions: float | None 
    duration: int | None 
    completed : bool = Field(default=False)

    workout_exercise_id: int = Field(default=None,foreign_key="workout_exercise.id")
    workout_exercise:  Workout_Exercise | None = Relationship(back_populates="sets")


class Meal(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str 
    recipe_url: str | None

    checklists: list["Meal_Checklist"] = Relationship(back_populates="meal")


class Meal_Checklist(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    meal_id: int | None = Field(default=None,foreign_key="meal.id")
    user_id: int = Field(foreign_key="user.id")
    
    meal: Meal | None  = Relationship(back_populates="checklists")
    user: User| None  = Relationship(back_populates="meals")
    meal_type: str | None 
    completed: bool = Field(default=False)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)






