from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi import security
import crud, models, schemas
from database import engine
from crud import get_db
from logging.config import dictConfig
from my_log_conf import log_config

dictConfig(log_config)

import logging

logger = logging.getLogger('foo-logger')

models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)


# Dependency

@app.get("/api/users/me", response_model=schemas.User)
def get_user(user: schemas.User = Depends(crud.get_current_user)):
    return user


# create endpoint to login a user
@app.post("/api/token")
def generate_token(
        form_data: security.OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    user = crud.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    return crud.create_token(user)

    # db_user = crud.get_user_by_email(db, email=user.email)
    # if db_user is None:
    #     raise HTTPException(status_code=404, detail="User not found")
    # if db_user.password != user.password:
    #     raise HTTPException(status_code=400, detail="Incorrect password")
    # return db_user


#


@app.post("/api/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/api/users", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/api/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# @app.post("/api/users/social", response_model=schemas.Social)
# def create_social_for_user(social: schemas.SocialCreate, db: Session = Depends(get_db),
#                            user: schemas.User = Depends(crud.get_current_user)):
#     # user_socials = crud.get_user_socials(db, user_id=user.id)
#     # if user_socials:
#     #     raise HTTPException(status_code=400, detail="Social already registered. Please update instead")
#     return crud.create_user_socials(db=db, social=social, user_id=user.id)


# endpoint to update user socials
@app.put("/api/users/socialUpdate", response_model=schemas.Social)
def update_social_for_user(social: schemas.SocialUpdate, db: Session = Depends(get_db),
                           user: schemas.User = Depends(crud.get_current_user)):
    return crud.update_user_socials(db=db, social=social, user=user)


@app.get("/api/users/{user_id}/social", response_model=schemas.Social)
def read_user_socials(user_id: int, db: Session = Depends(get_db)):
    socials = crud.get_user_socials(db, user_id=user_id)
    if not socials:
        raise HTTPException(status_code=404, detail="Social details not found")
    return socials


@app.post("/api/users/projects", response_model=schemas.Project)
def create_project_for_user(project: schemas.ProjectCreate, db: Session = Depends(get_db),
                            user: schemas.User = Depends(crud.get_current_user)):
    return crud.create_user_projects(db=db, project=project, user_id=user.id)


@app.get("/api/users/{user_id}/projects", response_model=list[schemas.Project])
def read_user_projects(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = crud.get_user_projects(db, user_id=user_id, skip=skip, limit=limit)
    return projects


# endpoint to update user projects
@app.put("/api/users/projectsUpdate/{project_id}", response_model=schemas.Project)
def update_project_for_user(project_id: int, project: schemas.ProjectCreate, db: Session = Depends(get_db),
                            user: schemas.User = Depends(crud.get_current_user)):
    return crud.update_user_projects(db=db, project=project, project_id=project_id, user=user)


