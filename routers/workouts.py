from fastapi import APIRouter,Depends, HTTPException
from models import User,Workout,Workout_Exercise,Workout_Exercise_Set,Exercise,Workout_Template,Workout_Template_Exercise
from dependencies import get_session,get_openai_client
from db_helper import create_object
from openai import OpenAI
from openai_models import WorkoutPlan
from openai_helper import create_user_workout_plan_prompt,get_parse_response_open_ai
from data_parsing_helper import parse_ai_workout_plan
import json 
from typing import Dict
from serializers import WorkoutTemplateRead,TemplateExerciseRead,WorkoutFromTemplateRead,WorkoutExerciseSetIncoming
from sqlmodel import  Session,select

router = APIRouter(
    prefix="/workouts",
    tags=["workouts"],
    dependencies=[Depends(get_session)]
)


@router.get("/user_workouts/{user_id}")
def read_user_workouts(*, session: Session = Depends(get_session),user_id:int):
    statement = select(Workout).where(Workout.user_id==user_id)
    results = session.exec(statement).all()
    return results



@router.post("/")
def create_workout(*, session: Session = Depends(get_session),workout:Workout):
    workout.user = session.get(User,workout.user_id)
    return create_object(session,Workout,workout)



@router.post("/workout_exercise")
def create_workout_exercise(*, session: Session = Depends(get_session),workout_exercise:Workout_Exercise):
    workout_exercise.workout = session.get(Workout,workout_exercise.workout_id)
    workout_exercise.exercise = session.get(Exercise,workout_exercise.exercise_id)
    return create_object(session,Workout_Exercise,workout_exercise)


@router.get("/workout_exercise/{workout_id}")
def read_workout_exercises(*, session: Session = Depends(get_session),workout_id:int):
    statement = select(Workout_Exercise).where(Workout_Exercise.workout_id==workout_id)
    results = session.exec(statement).all()
    return results



@router.post("/workout_exercise_set")
def create_workout_exercise_set(*, session: Session = Depends(get_session),workout_exercise_set:Workout_Exercise_Set):
    workout_exercise_set.workout_exercise = session.get(Workout_Exercise,workout_exercise_set.workout_exercise_id)
    return create_object(session,Workout_Exercise_Set,workout_exercise_set)


@router.get("/workout_exercise_set/{workout_exercise_id}")
def read_workout_exercises(*, session: Session = Depends(get_session),workout_exercise_id:int):
    statement = select(Workout_Exercise_Set).where(Workout_Exercise_Set.workout_exercise_id==workout_exercise_id)
    results = session.exec(statement).all()
    return results




@router.get("/workout_templates/{user_id}", response_model=list[WorkoutTemplateRead])
def read_user_workout_templates(*, session: Session = Depends(get_session),user_id:int):
    statement = select(Workout_Template).where(Workout_Template.user_id==user_id)
    templates = session.exec(statement).all()

    results = list()
    for template in templates:
        template_exercises = template.template_exercises
        template_exercises_read = list()
        for template_exercise in template_exercises:
            template_exercise_read = TemplateExerciseRead.model_validate(TemplateExerciseRead(
                id=template_exercise.exercise.id,
                name=template_exercise.exercise.name,
                category=template_exercise.exercise.category,
                muscle_group=template_exercise.exercise.muscle_group,
                weight=template_exercise.weight,
                repetitions=template_exercise.repetitions,
                duration=template_exercise.duration
            ))
            template_exercises_read.append(
                template_exercise_read
            )
        
        workout_template_read = WorkoutTemplateRead.model_validate(WorkoutTemplateRead(
                id=template.id,
                name=template.name,
                exercises=template_exercises_read
            ))
        results.append(
            workout_template_read
        )

    return results


@router.get("/start_workout_by_template/{workout_template_id}", response_model=Dict[int,WorkoutFromTemplateRead])
def start_workout_by_template(*, session: Session = Depends(get_session),workout_template_id:int):
    statement = session.get(Workout_Template,workout_template_id)
    if not statement:
        raise HTTPException(status_code=404, detail="Template not found")

    print(f"Template: {statement}")
    results = dict()
    for template_exercise in statement.template_exercises:
        template_exercise_read = WorkoutFromTemplateRead.model_validate(WorkoutFromTemplateRead(
            name=template_exercise.exercise.name,
            muscle_group=template_exercise.exercise.muscle_group,
            category=template_exercise.exercise.category,
            weight=template_exercise.weight,
            video_url=template_exercise.exercise.video_url,
            repetitions=template_exercise.repetitions,
            duration=template_exercise.duration
        ))

        results[template_exercise.exercise.id] = template_exercise_read

    return results


@router.post("/end_workout/{user_id}")
def end_workout(*, session: Session = Depends(get_session), user_id: int, workout_sets: list[WorkoutExerciseSetIncoming]):
    
    user = session.get(User, user_id)
    print(f"User: {user}")
    workout = Workout(user_id=user_id)
    workout.user = user
    workout = create_object(session, Workout, workout)
    
    exercises_dict = dict()
    for workout_set in workout_sets:
        if workout_set.exercise_id not in exercises_dict:
            exercise = session.get(Exercise, workout_set.exercise_id)
            if not exercise:
                raise HTTPException(status_code=404, detail=f"Exercise with id {workout_set.exercise_id} not found")
            workout_exercise = Workout_Exercise(workout_id=workout.id, exercise_id=exercise.id)
            workout_exercise.exercise = exercise
            workout_exercise.workout = workout
            workout_exercise = create_object(session, Workout_Exercise, workout_exercise)
            exercises_dict[workout_set.exercise_id] = workout_exercise

        workout_set_object = Workout_Exercise_Set(
            workout_exercise_id=exercises_dict[workout_set.exercise_id].id,
            weight=workout_set.weight,
            repetitions=workout_set.repetitions,
            duration=workout_set.duration,
            completed=workout_set.completed
        )
        workout_set_object.workout_exercise = exercises_dict[workout_set.exercise_id]
        create_object(session,Workout_Exercise_Set,workout_set_object)

    return {"message": "Workout sets recorded successfully"}




@router.post("/workout_templates/ai/{user_id}")
def create_workout_templates_ai(*,client:OpenAI= Depends(get_openai_client), session: Session = Depends(get_session),user_id:int):
    
    # First create the AI generated workout plan.
    user = session.get(User,user_id)
    user_workout_plan_prompt = create_user_workout_plan_prompt(user)
    user_workout_plan_response = get_parse_response_open_ai(client,user_workout_plan_prompt,WorkoutPlan)
    user_workout_plan_json = user_workout_plan_response.choices[0].message.content
    user_workout_plan_data = json.loads(user_workout_plan_json)
    #user_workout_plan_data = workout_test
    template_exercises_created = parse_ai_workout_plan(user_workout_plan_data,user,session)

    statement = select(Workout_Template).where(Workout_Template.user_id==user_id)
    results = session.exec(statement).all()
    return results

