from fastapi import APIRouter,Depends
from models import User
from dependencies import get_session
from sqlmodel import  Session

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_session)]
)


fake_users_db = [{"email":"juan.nunez.corp@gmail.com","weight":88,"height":182,"goal":"Build Muscle"}]


@router.get("/")
async def read_items():
    return fake_users_db


@router.post("/")
def create_user(*, session: Session = Depends(get_session),user:User):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
