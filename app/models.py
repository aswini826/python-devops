from .database import Base
from sqlalchemy.sql.sqltypes  import TIMESTAMP
from sqlalchemy.sql.expression  import text
from sqlalchemy import Column, Integer, String, Boolean

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    movie = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
