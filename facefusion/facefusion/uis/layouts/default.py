import gradio
from facefusion import state_manager
from facefusion.uis.components import (
    about, age_modifier_options, common_options, execution, execution_queue_count,
    execution_thread_count, expression_restorer_options, face_debugger_options,
    face_detector, face_editor_options, face_enhancer_options, face_landmarker,
    face_masker, face_selector, face_swapper_options, frame_colorizer_options,
    frame_enhancer_options, instant_runner, job_manager, job_runner, lip_syncer_options,
    memory, output, output_options, preview, processors, source, target, temp_frame,
    terminal, trim_frame, ui_workflow
)

def create_gradio_ui() -> gradio.Blocks:
    with gradio.Blocks() as layout:
        with gradio.Row():
            with gradio.Column(scale=4):
                with gradio.Blocks(): about.render()
                with gradio.Blocks(): processors.render()
                with gradio.Blocks(): age_modifier_options.render()
                with gradio.Blocks(): expression_restorer_options.render()
                with gradio.Blocks(): face_debugger_options.render()
                with gradio.Blocks(): face_editor_options.render()
                with gradio.Blocks(): face_enhancer_options.render()
                with gradio.Blocks(): face_swapper_options.render()
                with gradio.Blocks(): frame_colorizer_options.render()
                with gradio.Blocks(): frame_enhancer_options.render()
                with gradio.Blocks(): lip_syncer_options.render()
                with gradio.Blocks():
                    execution.render()
                    execution_thread_count.render()
                    execution_queue_count.render()
                with gradio.Blocks(): memory.render()
                with gradio.Blocks(): temp_frame.render()
                with gradio.Blocks(): output_options.render()
            with gradio.Column(scale=4):
                with gradio.Blocks(): source.render()
                with gradio.Blocks(): target.render()
                with gradio.Blocks(): output.render()
                with gradio.Blocks(): terminal.render()
                with gradio.Blocks():
                    ui_workflow.render()
                    instant_runner.render()
                    job_runner.render()
                    job_manager.render()
            with gradio.Column(scale=7):
                with gradio.Blocks(): preview.render()
                with gradio.Blocks(): trim_frame.render()
                with gradio.Blocks(): face_selector.render()
                with gradio.Blocks(): face_masker.render()
                with gradio.Blocks(): face_detector.render()
                with gradio.Blocks(): face_landmarker.render()
                with gradio.Blocks(): common_options.render()
    return layout
	
# facefusion/facefusion/uis/layouts/default.py
def launch_gradio_ui():
    # Your logic for launching the Gradio UI
    pass
