from uuid import UUID
from pgvector import Vector
from sqlalchemy import JSON, Column, Integer, String, ForeignKey, Text
from database import Base

class Users(Base):
    __tablename__ = 'users'
    id = Column(UUID, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class chats(Base):
    __tablename__ = 'chats'
    id = Column(UUID, primary_key=True, index=True, nullable=False)
    user_id = Column(UUID,ForeignKey('users.id'), nullable=False)
    
class sumaries(Base):
    __tablename__ = 'sumaries'
    id = Column(UUID, primary_key=True, index=True, nullable=False)
    chat_id = Column(UUID,ForeignKey('chats.id'), nullable=False)
    summary_text = Column(String, nullable=False)

class rag_entries(Base):
    __tablename__ = 'rag_entries'
    id = Column(UUID, primary_key=True, index=True, nullable=False)
    doc_id = Column(UUID, nullable=False)
    chunk_id = Column(UUID, nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector, nullable=False)
    metadata= Column(JSON, nullable=True)