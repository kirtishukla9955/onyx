import os
import uuid
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db, Asset, AssetStatus
from storage.s3_client import s3_storage
from models.schemas import UploadResponse

router = APIRouter(prefix="/api", tags=["Upload"])

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".mp4", ".mov", ".wav", ".mp3"}

def validate_file(filename: str):
    _, ext = os.path.splitext(filename.lower())
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    return ext

@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_asset(
    file: UploadFile = File(...),
    niche: str = Form(None),
    platform: str = Form(None),
    db: Session = Depends(get_db)
):
    # 1. Validate file extension
    ext = validate_file(file.filename)

    # 2. Generate unique filename for storage to prevent collisions
    asset_id = uuid.uuid4()
    unique_filename = f"{asset_id}{ext}"

    # 3. Read content and determine file size
    try:
        # Read file contents to upload
        file_content = await file.read()
        file_size = len(file_content)
        
        # Reset read pointer for upload_fileobj if needed, but since we have bytes, 
        # we can wrap it or just upload raw bytes using put_object
        # Let's wrap bytes in a BytesIO or use s3_storage.upload_protected_file
        import io
        file_like = io.BytesIO(file_content)
        
        # Upload to MinIO/S3
        file_url = s3_storage.upload_file(
            file_like, 
            unique_filename, 
            file.content_type or "application/octet-stream"
        )
    except Exception as s3_err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"S3/MinIO upload failed: {str(s3_err)}"
        )

    # 4. Save metadata to PostgreSQL
    try:
        new_asset = Asset(
            id=asset_id,
            filename=unique_filename,
            file_type=file.content_type or "application/octet-stream",
            file_size=file_size,
            original_url=file_url,
            status=AssetStatus.UPLOADED,
            niche=niche,
            platform=platform
        )
        db.add(new_asset)
        db.commit()
        db.refresh(new_asset)
    except Exception as db_err:
        # In a production app, we would clean up the uploaded S3 file here
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database save failed: {str(db_err)}"
        )

    return UploadResponse(
        asset_id=new_asset.id,
        status="uploaded",
        file_url=new_asset.original_url
    )
