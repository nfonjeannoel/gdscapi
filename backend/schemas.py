from pydantic import BaseModel


class SocialBase(BaseModel):
    blog: str | None = None
    github: str | None = None
    linkedin: str | None = None
    twitter: str | None = None
    portfolio: str | None = None


class SocialCreate(SocialBase):
    pass


class Social(SocialBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class ProjectBase(BaseModel):
    title: str
    description: str | None = None


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    socials: list[Social] | None = None
    projects: list[Project] = []
    name: str | None = None
    username: str | None = None
    avatar: str | None = None
    bio: str | None = None

    class Config:
        orm_mode = True


class UserLogin(UserBase):
    password: str


# update user schema
class UserUpdate(BaseModel):
    name: str | None = None
    username: str | None = None
    avatar: str | None = None
    bio: str | None = None

    class Config:
        orm_mode = True


# update social schema
class SocialUpdate(BaseModel):
    blog: str | None = None
    github: str | None = None
    linkedin: str | None = None
    twitter: str | None = None
    portfolio: str | None = None

    class Config:
        orm_mode = True
