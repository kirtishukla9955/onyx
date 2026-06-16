import hashlib
from sqlalchemy.orm import Session
from models import RecipientRegistry

def generate_payload(signature: str, recipient_name: str) -> str:
    """
    Generates a unique watermark payload for a specific recipient.
    """
    raw_str = f"{signature}::{recipient_name}"
    hashed = hashlib.sha256(raw_str.encode()).hexdigest()[:16] # Use first 16 chars for brevity
    return f"{signature}_{hashed}"

def register_recipient(db: Session, recipient_name: str, payload: str):
    """
    Stores the recipient name and their unique payload string in the database.
    Updates the payload if the recipient already exists.
    """
    existing = db.query(RecipientRegistry).filter(RecipientRegistry.recipient_name == recipient_name).first()
    if existing:
        existing.payload = payload
    else:
        new_record = RecipientRegistry(recipient_name=recipient_name, payload=payload)
        db.add(new_record)
    db.commit()

def trace_payload(db: Session, payload: str) -> str | None:
    """
    Queries the database to match the payload against stored records.
    Returns the recipient name if found, else None.
    """
    record = db.query(RecipientRegistry).filter(RecipientRegistry.payload == payload).first()
    if record:
        return record.recipient_name
    return None

def get_all_recipients(db: Session):
    """
    Returns a list of all recipients and their assigned payload identifiers.
    """
    return db.query(RecipientRegistry).all()
