import uuid
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from db.database import get_db, Asset, AssetStatus
from services.pipeline_service import run_protection_pipeline
from services.log_service import sse_log_generator

router = APIRouter(prefix="/api", tags=["Protection & Logs"])

@router.post("/protect/{asset_id}", status_code=status.HTTP_202_ACCEPTED)
def trigger_protection(
    asset_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Triggers the protection pipeline in the background and sets status to queued.
    """
    # 1. Verify asset exists
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found."
        )

    # 2. Check if asset is already processed or processing
    if asset.status in [AssetStatus.QUEUED, AssetStatus.PROCESSING]:
        return {
            "asset_id": asset.id,
            "status": asset.status,
            "message": "Asset protection is already in progress."
        }

    # 3. Initialize/reset status to queued in DB
    asset.status = AssetStatus.QUEUED
    db.commit()

    # 4. Trigger pipeline in the background
    background_tasks.add_task(run_protection_pipeline, asset.id)

    return {
        "asset_id": asset.id,
        "status": "queued",
        "message": "Protection pipeline triggered."
    }

@router.get("/logs/{asset_id}")
def stream_logs(
    asset_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Server-Sent Events (SSE) endpoint that streams logs for the given asset.
    """
    # Verify asset exists
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found."
        )

    return StreamingResponse(
        sse_log_generator(asset_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
