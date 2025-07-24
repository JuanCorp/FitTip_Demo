from pydantic import BaseModel
from enum import Enum 

class ExerciseCategoryEnum(str,Enum):
    weightlifting= "Weightlifting"
    cardio = "Cardio"
    flexibility = "Flexibility"
    bodyweight= "Bodyweight"


class Exercise(BaseModel):
    name:str
    category: ExerciseCategoryEnum
    muscle_group: str 
    video_url:str 
    weight: float | None 
    repetitions: int | None
    duration: int | None 

class Workout(BaseModel):
    exercises: list[Exercise]
    name: str

class WorkoutPlan(BaseModel):
    workouts: list[Workout]


class MealTypeEnum(str,Enum):
    breakfast="Breakfast"
    lunch="Lunch"
    Dinner="Dinner"

class Meal(BaseModel):
    name:str
    meal_type: MealTypeEnum
    description:str
    recipe_url:str 


class MealDay(BaseModel):
    meals: list[Meal]


class MealPlan(BaseModel):
    meal_days: list[MealDay]



class Conversation(BaseModel):
    message:str
    conversationHistory: list[dict] | None = None