from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gradio import mount_gradio_app
from facefusion_ui import create_gradio_ui  # Import Gradio UI function

app = FastAPI()

# CORS settings (optional, adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Gradio app on a specific route, e.g., "/facefusion"
gradio_app = create_gradio_ui()
app = mount_gradio_app(app, gradio_app, path="/facefusion")

@app.get("/")
async def root():
    return {"message": "FaceFusion API is running!"}
