from sqlalchemy.orm import Session

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_socials(db: Session, user_id: int):
    return db.query(models.Social).filter(models.Social.owner_id == user_id).all()


def get_social_by_user_id(db: Session, user_id: int):
    return db.query(models.Social).filter(models.Social.owner_id == user_id).first()


def create_user_socials(db: Session, social: schemas.SocialCreate, user_id: int):
    db_social = models.Social(**social.dict(), owner_id=user_id)
    db.add(db_social)
    db.commit()
    db.refresh(db_social)
    return db_social


def get_user_projects(db: Session, user_id: int, skip: int = 0, limit: int = 1000):
    return db.query(models.Project).filter(models.Project.owner_id == user_id).offset(skip).limit(limit).all()


def create_user_projects(db: Session, project: schemas.ProjectCreate, user_id: int):
    db_project = models.Project(**project.dict(), owner_id=user_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_user_socials(db: Session, social: schemas.SocialUpdate, user_id: int):
    db_social = db.query(models.Social).filter(models.Social.owner_id == user_id).first()
    db_social.github = social.github if social.github is not None else db_social.github
    db_social.linkedin = social.linkedin if social.linkedin is not None else db_social.linkedin
    db_social.twitter = social.twitter if social.twitter is not None else db_social.twitter
    db_social.portfolio = social.portfolio if social.portfolio is not None else db_social.portfolio
    db_social.blog = social.blog if social.blog is not None else db_social.blog
    db.commit()
    db.refresh(db_social)
    return db_social

