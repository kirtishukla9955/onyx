import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db, Asset
from models.schemas import ResultsResponse

router = APIRouter(prefix="/api", tags=["Results & Verification"])

@router.get("/results/{asset_id}", response_model=ResultsResponse)
def get_results(
    asset_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Returns the complete asset record, including URLs, watermark, status, and logs.
    """
    # Fetch asset and load logs relationship
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found."
        )
        
    return asset
