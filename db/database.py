import os
import uuid
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, BigInteger, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Get DATABASE_URL from env or use a default
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/onyx"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AssetStatus(str):
    UPLOADED = "uploaded"
    QUEUED = "queued"
    PROCESSING = "processing"
    PROTECTED = "protected"
    FAILED = "failed"

class Asset(Base):
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(BigInteger, nullable=False)
    original_url = Column(String, nullable=True)
    protected_url = Column(String, nullable=True)
    watermark_id = Column(String, nullable=True)
    status = Column(
        String, 
        default=AssetStatus.UPLOADED, 
        nullable=False
    )
    niche = Column(String, nullable=True)
    platform = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow, 
        nullable=False
    )

    # Relationships
    logs = relationship("ProcessingLog", back_populates="asset", cascade="all, delete-orphan")

class ProcessingLog(Base):
    __tablename__ = "processing_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    log_line = Column(String, nullable=False)
    emitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    asset = relationship("Asset", back_populates="logs")

# DB Dependency injection helper
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
