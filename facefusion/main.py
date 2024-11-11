import sys
import os

# Add the 'facefusion' directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'facefusion'))


from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

# facefusion/main.py
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "FaceFusion API is running!"}

@app.get("/facefusion")
async def gradio_interface():
    # Defer the import to avoid circular import
    try:
        from facefusion.uis.layouts.default import create_gradio_ui  # Correct path
        gradio_app = create_gradio_ui()
        gradio_app.launch(share=False)  # Change to `share=True` if needed for testing
        return JSONResponse(content={"message": "Gradio interface launched"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
