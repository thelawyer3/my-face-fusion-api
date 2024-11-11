from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from facefusion.uis.layouts.default import create_gradio_ui  # Import Gradio UI function from default.py
from facefusion.core import launch  # This function launches Gradio with state_manager configurations

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "FaceFusion API is running!"}

@app.get("/facefusion")
async def gradio_interface():
    # Launch the Gradio interface
    try:
        gradio_app = create_gradio_ui()
        gradio_app.launch(share=False)  # Change to `share=True` if needed for testing
        return JSONResponse(content={"message": "Gradio interface launched"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
