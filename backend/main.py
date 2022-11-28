from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/social/", response_model=schemas.Social)
def create_social_for_user(user_id: int, social: schemas.SocialCreate, db: Session = Depends(get_db)):
    return crud.create_user_socials(db=db, social=social, user_id=user_id)


@app.get("/users/{user_id}/social/", response_model=list[schemas.Social])
def read_user_socials(user_id: int, db: Session = Depends(get_db)):
    socials = crud.get_user_socials(db, user_id=user_id)
    return socials


@app.post("/users/{user_id}/projects/", response_model=schemas.Project)
def create_project_for_user(user_id: int, project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_user_projects(db=db, project=project, user_id=user_id)


@app.get("/users/{user_id}/projects/", response_model=list[schemas.Project])
def read_user_projects(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = crud.get_user_projects(db, user_id=user_id, skip=skip, limit=limit)
    return projects


# create endpoint to login a user
@app.post("/login/", response_model=schemas.User)
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.password != user.password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    return db_user


# endpoint to update user socials
@app.put("/users/{user_id}/socialUpdate/", response_model=schemas.Social)
def update_social_for_user(user_id: int, social: schemas.SocialUpdate, db: Session = Depends(get_db)):
    return crud.update_user_socials(db=db, social=social, user_id=user_id)
