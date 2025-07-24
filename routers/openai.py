from fastapi import APIRouter,Depends, UploadFile
from dependencies import get_session,get_openai_client
from openai import OpenAI
from openai_models import MealPlan,Conversation
from data_parsing_helper import parse_ai_meal_plan
from openai_helper import create_baseline_prompt, get_response_open_ai,create_prompt
from sqlmodel import  Session,select
from video_parsing import extract_frames
import json
from fastapi.responses import StreamingResponse
import os

router = APIRouter(
    prefix="/openai",
    tags=["openai"],
    dependencies=[Depends(get_session)]
)


fake_users_db = [{"email":"juan.nunez.corp@gmail.com","weight":88,"height":182,"goal":"Build Muscle"}]


@router.post("/video_parse")
def stream_gpt_response(*,client:OpenAI=Depends(get_openai_client),video: UploadFile):  
    frame_interval = 20 
    video_temp_path = f"temp_videos/{video.filename}"
    with open(video_temp_path,"wb") as f:
        f.write(video.file.read())

    frames = extract_frames(video_temp_path, frame_interval)
    if os.path.exists(video_temp_path):
        os.remove(video_temp_path)
    

    return StreamingResponse(get_response_open_ai(client,create_baseline_prompt(frames)), media_type="text/event-stream")



@router.post("/chat")
def stream_gpt_response(*,client:OpenAI=Depends(get_openai_client),conversation:Conversation):   
    return StreamingResponse(get_response_open_ai(client,create_prompt(conversation)), media_type="text/event-stream")




