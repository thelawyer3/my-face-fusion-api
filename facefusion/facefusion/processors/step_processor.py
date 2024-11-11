# facefusion/processors/step_processor.py

def process_step(job_id: str, step_index: int, step_args: Args) -> bool:
    clear_reference_faces()
    step_total = job_manager.count_step_total(job_id)
    step_args.update(collect_job_args())
    apply_args(step_args, state_manager.set_item)

    logger.info(wording.get('processing_step').format(step_current=step_index + 1, step_total=step_total), __name__)
    if common_pre_check() and processors_pre_check():
        error_code = conditional_process()
        return error_code == 0
    return False
