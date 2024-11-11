from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import shutil
import os
from uuid import uuid4

app = FastAPI()

# Directories to store uploaded and processed files
UPLOAD_DIR = "uploads/"
PROCESSED_DIR = "processed/"

# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "FaceFusion API is running!"}

@app.post("/upload")
async def upload_files(
    target_source: UploadFile = File(...),
    target_video: UploadFile = File(...),
    face_mask_value: int = Form(...)
):
    # Generate unique identifiers for files
    source_file_id = str(uuid4())
    video_file_id = str(uuid4())
    
    # Save Target Source Image
    source_file_location = f"{UPLOAD_DIR}{source_file_id}_{target_source.filename}"
    with open(source_file_location, "wb") as buffer:
        shutil.copyfileobj(target_source.file, buffer)

    # Save Target Video
    video_file_location = f"{UPLOAD_DIR}{video_file_id}_{target_video.filename}"
    with open(video_file_location, "wb") as buffer:
        shutil.copyfileobj(target_video.file, buffer)

    # Log the face mask value
    print(f"Face Mask Value: {face_mask_value}")

    # Return file locations and face mask for reference
    return JSONResponse(content={
        "source_file_location": source_file_location,
        "video_file_location": video_file_location,
        "face_mask_value": face_mask_value
    })

@app.post("/process")
async def process_video(
    source_file_location: str = Form(...),
    video_file_location: str = Form(...),
    face_mask_value: int = Form(...)
):
    # Verify that both files exist
    if not os.path.exists(source_file_location) or not os.path.exists(video_file_location):
        raise HTTPException(status_code=404, detail="File not found")

    # Placeholder for processing logic
    # Use source_file_location, video_file_location, and face_mask_value to perform face swap
    # Currently, we simulate processing by copying the file to PROCESSED_DIR
    processed_video_file = f"{PROCESSED_DIR}processed_{os.path.basename(video_file_location)}"
    shutil.copyfile(video_file_location, processed_video_file)

    # This is where you'd integrate the FaceFusion face-swapping function

    return JSONResponse(content={
        "processed_video_location": processed_video_file
    })

@app.get("/download")
async def download_video(processed_video_location: str):
    # Verify that the processed file exists
    if not os.path.exists(processed_video_location):
        raise HTTPException(status_code=404, detail="Processed file not found")
    
    # Serve the processed file for download
    return FileResponse(path=processed_video_location, filename=os.path.basename(processed_video_location))

# Run the API with: uvicorn main:app --reload
