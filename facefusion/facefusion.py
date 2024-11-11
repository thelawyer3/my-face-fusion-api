import os
import gradio as gr
from facefusion.uis.layouts.default import create_gradio_ui  # Correct path to your Gradio UI function

# Get the port from the environment variable provided by Render, default to 7860 if not set
port = os.getenv("PORT", 7860)

# Create the Gradio interface using the function
gradio_app = create_gradio_ui()

# Launch the Gradio app on the appropriate port
gradio_app.launch(server_name="0.0.0.0", server_port=port, share=False)  # share=True if you need public link
