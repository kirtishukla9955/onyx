from sqlalchemy import Column, Integer, String
from database import Base

class RecipientRegistry(Base):
    __tablename__ = "recipient_registry"

    id = Column(Integer, primary_key=True, index=True)
    recipient_name = Column(String, unique=True, index=True, nullable=False)
    payload = Column(String, unique=True, nullable=False)
