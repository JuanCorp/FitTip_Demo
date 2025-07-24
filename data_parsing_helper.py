import models
from sqlmodel import  select
from db_helper import create_object

def parse_ai_workout_plan(workout_plan,user,session):
    template_exercises_created= list()
    for workout in workout_plan['workouts']:
        name = workout['name']
        print(user.id)
        template_object = models.Workout_Template(name=name,user_id=user.id)
        template_object.user = user
        template = create_object(session,models.Workout_Template,template_object)

        for exercise in workout["exercises"]:
            statement = select(models.Exercise).where(models.Exercise.name==exercise["name"])
            exercise_created = session.exec(statement).first()
            if exercise_created is None:
                # New Exercise Create 
                exercise_object = models.Exercise(name=exercise["name"],category=exercise["category"],muscle_group=exercise["muscle_group"],
                                                  video_url=exercise["video_url"])
                exercise_created = create_object(session,models.Exercise,exercise_object)
            

            workout_template_exercise_object = models.Workout_Template_Exercise(
                template=template,
                exercise=exercise_created,
                weight=exercise["weight"],
                repetitions=exercise["repetitions"],
                duration=exercise["duration"]
            )
            print(workout_template_exercise_object)
            workout_template_exercise_created = create_object(session,models.Workout_Template_Exercise,workout_template_exercise_object)
            template_exercises_created.append(workout_template_exercise_created)
    
    return template_exercises_created



def parse_ai_meal_plan(meal_plan,user,session):
    meal_checklist_created= list()
    for meal_day in meal_plan['meal_days']:
        for meal in meal_day['meals']:
            statement = select(models.Meal).where(models.Meal.name==meal["name"])
            meal_created = session.exec(statement).first()
            if meal_created is None:
                # New Meal Create 
                meal_object = models.Meal(name=meal["name"],description=meal["description"],
                                                    recipe_url=meal["recipe_url"])
                meal_created = create_object(session,models.Meal,meal_object)
                
            meal_checklist_object = models.Meal_Checklist(
                    meal=meal_created,
                    user_id=user.id,
                    meal_type=meal["meal_type"]
                )
            meal_checklist_object.user=user
            meal_checklist_object_created = create_object(session,models.Meal_Checklist,meal_checklist_object)
            meal_checklist_created.append(meal_checklist_object_created)
        
    return meal_checklist_created






