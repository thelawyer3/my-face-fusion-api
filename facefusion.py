import os
from facefusion import core
import gradio as gr

# Set environment variables for threading if needed
os.environ['OMP_NUM_THREADS'] = '1'

def main():
    print("Starting FaceFusion Application...")  # Debugging log

    # Placeholder Gradio app
    def greet(name):
        return f"Hello, {name}!"
    
    app = gr.Interface(fn=greet, inputs="text", outputs="text")
    print("Launching Gradio app on port 8080...")  # Debugging log
    app.launch(server_port=8080)  # Ensure the server is bound to port 8080

if __name__ == '__main__':
    main()
