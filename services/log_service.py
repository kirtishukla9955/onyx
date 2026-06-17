import time
import json
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from db.database import SessionLocal, Asset, ProcessingLog

def write_log(db: Session, asset_id: uuid.UUID, log_line: str) -> ProcessingLog:
    """
    Writes a single log line to the processing_logs table.
    """
    log_entry = ProcessingLog(
        asset_id=asset_id,
        log_line=log_line,
        emitted_at=datetime.utcnow()
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry

def get_asset_logs(db: Session, asset_id: uuid.UUID):
    """
    Fetches all logs associated with an asset.
    """
    return db.query(ProcessingLog).filter(
        ProcessingLog.asset_id == asset_id
    ).order_by(ProcessingLog.id.asc()).all()

def sse_log_generator(asset_id: uuid.UUID):
    """
    Generator for Server-Sent Events. Queries database for new logs and yields
    them in real-time, closing when the pipeline completes or fails.
    """
    db = SessionLocal()
    last_log_id = 0
    try:
        # Check if asset exists first
        asset = db.query(Asset).filter(Asset.id == asset_id).first()
        if not asset:
            yield f"data: {json.dumps({'error': 'Asset not found'})}\n\n"
            return

        # Start streaming
        while True:
            # Fetch new logs written after last_log_id
            new_logs = db.query(ProcessingLog).filter(
                ProcessingLog.asset_id == asset_id,
                ProcessingLog.id > last_log_id
            ).order_by(ProcessingLog.id.asc()).all()

            for log in new_logs:
                last_log_id = log.id
                yield f"data: {json.dumps({'log_line': log.log_line, 'emitted_at': log.emitted_at.isoformat()})}\n\n"

            # Check status of the asset
            db.refresh(asset)
            if asset.status in ["protected", "failed"]:
                # Ensure no logs were written in the split second before finishing
                extra_logs = db.query(ProcessingLog).filter(
                    ProcessingLog.asset_id == asset_id,
                    ProcessingLog.id > last_log_id
                ).order_by(ProcessingLog.id.asc()).all()
                
                for log in extra_logs:
                    last_log_id = log.id
                    yield f"data: {json.dumps({'log_line': log.log_line, 'emitted_at': log.emitted_at.isoformat()})}\n\n"
                
                break

            time.sleep(0.5)  # Poll the database every 500ms
    except Exception as e:
        yield f"data: {json.dumps({'error': f'Stream error: {str(e)}'})}\n\n"
    finally:
        db.close()
