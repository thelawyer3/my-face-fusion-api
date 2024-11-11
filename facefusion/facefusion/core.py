from functools import lru_cache
import shutil
import signal
import sys
from time import time

import numpy
from facefusion import content_analyser, face_classifier, face_detector, face_landmarker, face_masker, face_recognizer, logger, process_manager, state_manager, voice_extractor, wording
from facefusion.args import apply_args, collect_job_args, reduce_step_args
from facefusion.common_helper import get_first
from facefusion.content_analyser import analyse_image, analyse_video
from facefusion.download import conditional_download_hashes, conditional_download_sources
from facefusion.exit_helper import conditional_exit, graceful_exit, hard_exit
from facefusion.face_analyser import get_average_face, get_many_faces, get_one_face
from facefusion.face_selector import sort_and_filter_faces
from facefusion.face_store import append_reference_face, clear_reference_faces, get_reference_faces
from facefusion.ffmpeg import copy_image, extract_frames, finalize_image, merge_video, replace_audio, restore_audio
from facefusion.filesystem import filter_audio_paths, is_image, is_video, list_directory, resolve_relative_path
from facefusion.jobs import job_helper, job_manager, job_runner
from facefusion.jobs.job_list import compose_job_list
from facefusion.memory import limit_system_memory
from facefusion.processors.core import get_processors_modules
from facefusion.program import create_program
from facefusion.program_helper import validate_args
from facefusion.statistics import conditional_log_statistics
from facefusion.temp_helper import clear_temp_directory, create_temp_directory, get_temp_file_path, get_temp_frame_paths, move_temp_file
from facefusion.typing import Args, ErrorCode
from facefusion.vision import get_video_frame, pack_resolution, read_image, read_static_images, restrict_image_resolution, restrict_video_fps, restrict_video_resolution, unpack_resolution


def cli() -> None:
    signal.signal(signal.SIGINT, lambda signal_number, frame: graceful_exit(0))
    program = create_program()

    if validate_args(program):
        args = vars(program.parse_args())
        apply_args(args, state_manager.init_item)

        if state_manager.get_item('command'):
            logger.init(state_manager.get_item('log_level'))
            route(args)
        else:
            program.print_help()


def route(args : Args) -> None:
    system_memory_limit = state_manager.get_item('system_memory_limit')
    if system_memory_limit and system_memory_limit > 0:
        limit_system_memory(system_memory_limit)
    if state_manager.get_item('command') == 'force-download':
        error_code = force_download()
        return conditional_exit(error_code)
    if state_manager.get_item('command') in [ 'job-list', 'job-create', 'job-submit', 'job-submit-all', 'job-delete', 'job-delete-all', 'job-add-step', 'job-remix-step', 'job-insert-step', 'job-remove-step' ]:
        if not job_manager.init_jobs(state_manager.get_item('jobs_path')):
            hard_exit(1)
        error_code = route_job_manager(args)
        hard_exit(error_code)
    if not pre_check():
        return conditional_exit(2)
    if state_manager.get_item('command') == 'run':
        import facefusion.uis.core as ui

        if not common_pre_check() or not processors_pre_check():
            return conditional_exit(2)
        for ui_layout in ui.get_ui_layouts_modules(state_manager.get_item('ui_layouts')):
            if not ui_layout.pre_check():
                return conditional_exit(2)
        ui.launch()
    if state_manager.get_item('command') == 'headless-run':
        if not job_manager.init_jobs(state_manager.get_item('jobs_path')):
            hard_exit(1)
        error_core = process_headless(args)
        hard_exit(error_core)
    if state_manager.get_item('command') in [ 'job-run', 'job-run-all', 'job-retry', 'job-retry-all' ]:
        if not job_manager.init_jobs(state_manager.get_item('jobs_path')):
            hard_exit(1)
        error_code = route_job_runner()
        hard_exit(error_code)


def processors_pre_check() -> bool:
    # Get the processors list from state_manager
    processors = state_manager.get_item('processors')
    
    # If processors is None or not set, initialize it to an empty list to prevent errors
    if not processors:
        processors = []  # Fallback to an empty list if processors are not initialized

    if not isinstance(processors, list):
        logger.error("Processors not properly configured or initialized.", __name__)
        return False

    for processor_module in get_processors_modules(processors):
        if not processor_module.pre_check():
            return False
    return True


def get_processors_modules(available_processors):
    if not available_processors:
        raise ValueError("available_processors is None or empty. Ensure that the processors are properly initialized.")
    
    processor_modules = []

    for processor in available_processors:
        try:
            processor_module = importlib.import_module(f"facefusion.processors.modules.{processor}")
            processor_modules.append(processor_module)
        except ImportError:
            logger.error(f"Processor module {processor} could not be imported.", __name__)

    return processor_modules


def common_pre_check() -> bool:
    modules =\
    [
        content_analyser,
        face_classifier,
        face_detector,
        face_landmarker,
        face_masker,
        face_recognizer,
        voice_extractor
    ]

    return all(module.pre_check() for module in modules)


# The rest of the functions follow...
