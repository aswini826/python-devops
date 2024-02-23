from .database import Base
from sqlalchemy.sql.expression import null
from sqlalchemy import Column, Integer, String, Boolean

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    movie = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
