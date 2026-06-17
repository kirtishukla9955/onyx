from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import Response, JSONResponse
from sqlalchemy.orm import Session
import database
import models
import watermark
import tamper
import traitor

# Initialize database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="ONYX Cybersecurity Backend",
    description="Backend for ONYX creator protection platform",
    version="1.0.0"
)

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/embed-watermark")
async def api_embed_watermark(
    image: UploadFile = File(...), 
    signature: str = Form(...)
):
    try:
        image_bytes = await image.read()
        watermarked_bytes = watermark.embed_lsb(image_bytes, signature)
        
        return Response(content=watermarked_bytes, media_type="image/png", headers={
            "Content-Disposition": f"attachment; filename=watermarked_{image.filename}"
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/extract-watermark")
async def api_extract_watermark(image: UploadFile = File(...)):
    try:
        image_bytes = await image.read()
        extracted_text = watermark.extract_lsb(image_bytes)
        
        if extracted_text is None:
            return JSONResponse(status_code=404, content={"message": "No watermark detected."})
            
        return {"watermark": extracted_text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/verify-integrity")
async def api_verify_integrity(
    original_image: UploadFile = File(...),
    suspect_image: UploadFile = File(...)
):
    try:
        original_bytes = await original_image.read()
        suspect_bytes = await suspect_image.read()
        
        result = tamper.verify_integrity(original_bytes, suspect_bytes)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/generate-recipient-copy")
async def api_generate_recipient_copy(
    image: UploadFile = File(...),
    recipient_name: str = Form(...),
    signature: str = Form("ONYX_OWNER_001"),
    db: Session = Depends(get_db)
):
    try:
        image_bytes = await image.read()
        
        # Generate unique payload
        payload = traitor.generate_payload(signature, recipient_name)
        
        # Save to database
        traitor.register_recipient(db, recipient_name, payload)
        
        # Embed payload
        watermarked_bytes = watermark.embed_lsb(image_bytes, payload)
        
        return Response(content=watermarked_bytes, media_type="image/png", headers={
            "Content-Disposition": f"attachment; filename=recipient_{recipient_name}.png"
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/trace-leak")
async def api_trace_leak(
    leaked_image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        image_bytes = await leaked_image.read()
        extracted_payload = watermark.extract_lsb(image_bytes)
        
        if extracted_payload is None:
            return JSONResponse(status_code=404, content={"message": "No watermark detected."})
            
        # Trace payload in DB
        recipient_name = traitor.trace_payload(db, extracted_payload)
        
        if recipient_name:
            return {"recipient_name": recipient_name, "payload": extracted_payload}
        else:
            return JSONResponse(status_code=404, content={"message": "Payload unrecognised"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/recipients")
def api_get_recipients(db: Session = Depends(get_db)):
    try:
        recipients = traitor.get_all_recipients(db)
        return [{"id": r.id, "recipient_name": r.recipient_name, "payload": r.payload} for r in recipients]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
