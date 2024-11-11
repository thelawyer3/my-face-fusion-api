import os
from facefusion import core
import gradio as gr

# Set environment variables for threading if needed
os.environ['OMP_NUM_THREADS'] = '1'

def main():
    # Replace `core.cli()` with Gradio app launch code
    # Define your Gradio app here. For example, a placeholder Gradio interface:
    def greet(name):
        return f"Hello, {name}!"

    app = gr.Interface(fn=greet, inputs="text", outputs="text")
    app.launch(server_port=8080)

if __name__ == '__main__':
    main()
