from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import models, schemas
import fastapi.security as _security
import jwt as _jwt
import passlib.hash as _hash
import database

import logging

logger = logging.getLogger('foo-logger')

oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")

JWT_SECRET = "gdscbackend"


def create_database():
    return database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, password=_hash.bcrypt.hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2schema),
):
    logger.debug("Token: %s", token)
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(models.User).get(payload["id"])
    except:
        raise HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )

    return schemas.User.from_orm(user)


def create_token(user: models.User):
    user_obj = schemas.User.from_orm(user)

    token = _jwt.encode(user_obj.dict(), JWT_SECRET)

    return dict(access_token=token, token_type="bearer")


def get_user_socials(db: Session, user_id: int):
    return db.query(models.Social).filter(models.User.id == user_id).first()


# def get_social_by_user_id(db: Session, user_id: int):
#     return db.query(models.Social).filter(models.Social.owner_id == user_id).first()


def create_user_socials(db: Session, social: schemas.SocialCreate, user_id: int):
    db_social = models.Social(**social.dict(), owner_id=user_id)
    db.add(db_social)
    db.commit()
    db.refresh(db_social)
    return db_social


def get_user_projects(db: Session, user_id: int, skip: int = 0, limit: int = 1000):
    return db.query(models.Project).filter(models.Project.owner_id == user_id).offset(skip).limit(limit).all()


def update_user_projects(db: Session, project: schemas.ProjectCreate, project_id: int, user: schemas.User):
    db_project = db.query(models.Project).filter_by(owner_id=user.id).filter(models.Project.id == project_id).first()

    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    db_project.title = project.title
    db_project.description = project.description
    db.commit()
    db.refresh(db_project)


def create_user_projects(db: Session, project: schemas.ProjectCreate, user_id: int):
    db_project = models.Project(**project.dict(), owner_id=user_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_user_socials(db: Session, social: schemas.SocialUpdate, user: schemas.User):
    db_social = db.query(models.Social).filter(models.Social.owner_id == user.id).first()
    if not db_social:
        # create new socials
        db_social = models.Social(**social.dict(), owner_id=user.id)
        db.add(db_social)
        db.commit()
        db.refresh(db_social)
        return db_social

    db_social.blog = social.blog if social.blog is not None else db_social.blog
    db_social.github = social.github if social.github is not None else db_social.github
    db_social.twitter = social.twitter if social.twitter is not None else db_social.twitter
    db_social.linkedin = social.linkedin if social.linkedin is not None else db_social.linkedin
    db_social.portfolio = social.portfolio if social.portfolio is not None else db_social.portfolio

    db.commit()
    db.refresh(db_social)
    return db_social
    # db.commit()
    # db.refresh(updated_user)
    # x = schemas.Social.from_orm(user.socials)
    # logger.debug("Socials: %s", x)
    # db_social = db.query(models.Social).filter_by(owner_id=user.id).first()
    # if not db_social:
    #     new_social = schemas.SocialCreate(**social.dict())
    #     return create_user_socials(db=db, social=new_social, user_id=user.id)
    #
    # logger.debug("Social: %s", db_social.dict())
    #
    # db_social.github = social.github if social.github is not None else db_social.github
    # db_social.linkedin = social.linkedin if social.linkedin is not None else db_social.linkedin
    # db_social.twitter = social.twitter if social.twitter is not None else db_social.twitter
    # db_social.portfolio = social.portfolio if social.portfolio is not None else db_social.portfolio
    #
    # db.commit()
    # db.refresh(db_social)
    # return social.from_orm(db_social)


def authenticate_user(email: str, password: str, db: Session):
    user = get_user_by_email(db=db, email=email)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user
