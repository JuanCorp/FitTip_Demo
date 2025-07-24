from models import User,Exercise
import json

object_dict = {
    "User":User,
    "Exercise":Exercise
}

def create_object(session,model,object):
    db_object = model.model_validate(object)
    session.add(db_object)
    session.commit()
    session.refresh(db_object)
    return db_object


def initiate_db(session):
    with open("defaults_database.json","r") as db:
        data = json.load(db)
    
    for record in data:
        data_model = object_dict[record["model"]]
        create_object(session,data_model,data_model(**record["data"]))
