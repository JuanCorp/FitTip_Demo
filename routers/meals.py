from fastapi import APIRouter,Depends
from models import Meal,Meal_Checklist,User
from dependencies import get_session,get_openai_client
from openai import OpenAI
from openai_models import MealPlan
from data_parsing_helper import parse_ai_meal_plan
from openai_helper import create_user_meal_plan_prompt, get_parse_response_open_ai
from serializers import MealChecklistRead
from sqlmodel import  Session,select
import json

router = APIRouter(
    prefix="/meals",
    tags=["meals"],
    dependencies=[Depends(get_session)]
)


fake_users_db = [{"email":"juan.nunez.corp@gmail.com","weight":88,"height":182,"goal":"Build Muscle"}]


@router.get("/")
def list_meals(*, session: Session = Depends(get_session)):
    statement = select(Meal)
    results = session.exec(statement).all()
    return results


@router.post("/meal_plan/ai/{user_id}")
def create_meal_checklists_ai(*,client:OpenAI= Depends(get_openai_client), session: Session = Depends(get_session),user_id:int):
    
    # First create the AI generated meal plan.
    user = session.get(User,user_id)
    user_meal_plan_prompt = create_user_meal_plan_prompt(user)
    user_meal_plan_response = get_parse_response_open_ai(client,user_meal_plan_prompt,MealPlan)
    user_meal_plan_json = user_meal_plan_response.choices[0].message.content
    user_meal_plan_data = json.loads(user_meal_plan_json)
    template_meals_created = parse_ai_meal_plan(user_meal_plan_data,user,session)

    statement = select(Meal_Checklist).where(Meal_Checklist.user_id==user_id)
    results = session.exec(statement).all()
    return results



@router.get("/{user_id}", response_model=list[MealChecklistRead])
def list_user_meal_checklist(*, session: Session = Depends(get_session),user_id:int):
    statement = select(Meal_Checklist).where(Meal_Checklist.user_id==user_id)
    checklists = session.exec(statement).all()

    results = list()
    for checklist in checklists:
        meal = checklist.meal
        meal_checklist_read = MealChecklistRead.model_validate(MealChecklistRead(
                id=checklist.id,
                name=meal.name,
                description=meal.description,
                recipe_url=meal.recipe_url,
                meal_type=checklist.meal_type,
                completed=checklist.completed
            ))
        
        results.append(
            meal_checklist_read
        )

    return results

