from pydantic import BaseModel,ConfigDict,Field
from datetime import datetime


class MealChecklistRead(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    id: int 
    name: str 
    description: str
    recipe_url: str | None
    meal_type: str
    completed: bool


class TemplateExerciseRead(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    category: str
    muscle_group: str
    weight: float | None = None
    repetitions: int | None = None
    duration: int | None = None


class WorkoutTemplateRead(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    id: int 
    name: str 
    exercises: list[TemplateExerciseRead]



class WorkoutFromTemplateRead(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    name:str
    muscle_group: str
    category: str
    weight: float | None = None
    video_url: str | None = None
    repetitions: int | None = None
    duration: int | None = None
    sets: int |None = Field(default=3)


class WorkoutExerciseSetIncoming(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    exercise_id: int
    weight: float | None = None
    repetitions: int | None = None
    duration: int | None = None
    video_url: str | None = None
    completed: bool = False