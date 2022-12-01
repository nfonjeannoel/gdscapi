from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base
import passlib.hash as _hash


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String, index=True)
    username = Column(String, index=True)
    avatar = Column(String, index=True)
    bio = Column(String, index=True)

    socials = relationship("Social", back_populates="owner")
    projects = relationship("Project", back_populates="owner")

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.password)

    def __str__(self):
        return f"""
        email: {self.email}
        name: {self.name}
        username: {self.username}
        avatar: {self.avatar}
        bio: {self.bio}
        socials: {self.socials}
        projects: {self.projects}
        """


class Social(Base):
    __tablename__ = "socials"

    id = Column(Integer, primary_key=True, index=True)
    blog = Column(String)
    github = Column(String)
    linkedin = Column(String)
    twitter = Column(String)
    portfolio = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="socials")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="projects")
