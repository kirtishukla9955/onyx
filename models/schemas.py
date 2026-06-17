from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, List

class AssetBase(BaseModel):
    filename: str
    file_type: str
    file_size: int
    niche: Optional[str] = None
    platform: Optional[str] = None

class AssetCreate(AssetBase):
    pass

class AssetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    filename: str
    file_type: str
    file_size: int
    original_url: Optional[str] = None
    protected_url: Optional[str] = None
    watermark_id: Optional[str] = None
    status: str
    niche: Optional[str] = None
    platform: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class UploadResponse(BaseModel):
    asset_id: UUID
    status: str
    file_url: Optional[str] = None

class LogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    asset_id: UUID
    log_line: str
    emitted_at: datetime

class TrendTopic(BaseModel):
    trend_name: str
    predicted_peak_in_hours: int
    engagement_velocity_score: float
    niche_prompt: str

class TrendResponse(BaseModel):
    niche: Optional[str] = None
    platform: Optional[str] = None
    trends: List[TrendTopic]

class ResultsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    filename: str
    file_type: str
    file_size: int
    original_url: Optional[str] = None
    protected_url: Optional[str] = None
    watermark_id: Optional[str] = None
    status: str
    niche: Optional[str] = None
    platform: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    logs: List[LogResponse]

class HealthResponse(BaseModel):
    status: str
    version: str
