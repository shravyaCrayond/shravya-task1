from sqlalchemy import Column, Integer, String, DateTime, Text, func
from ..db.session import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(32), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)  # user input
    content = Column(Text, nullable=False)  # LLM response
    created_at = Column(DateTime(timezone=True), server_default=func.now())
