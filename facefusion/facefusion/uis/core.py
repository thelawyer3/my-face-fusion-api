import importlib
import os
import warnings
from types import ModuleType
from typing import Any, Dict, List, Optional

import gradio
from gradio.themes import Size

from facefusion import logger, metadata, state_manager, wording
from facefusion.exit_helper import hard_exit
from facefusion.filesystem import resolve_relative_path
from facefusion.uis import overrides
from facefusion.uis.typing import Component, ComponentName
from facefusion.uis.component_registry import get_ui_component, register_ui_component  # Import corrected component functions

# Disable Gradio analytics and suppress warnings
os.environ['GRADIO_ANALYTICS_ENABLED'] = '0'
warnings.filterwarnings('ignore', category=UserWarning, module='gradio')

# Override Gradio functions with custom implementations
gradio.processing_utils.encode_array_to_base64 = overrides.encode_array_to_base64
gradio.processing_utils.encode_pil_to_base64 = overrides.encode_pil_to_base64

UI_LAYOUT_MODULES: List[ModuleType] = []
UI_LAYOUT_METHODS = ['pre_check', 'render', 'listen', 'run']

def load_ui_layout_module(ui_layout: str) -> Any:
    try:
        ui_layout_module = importlib.import_module('facefusion.uis.layouts.' + ui_layout)
        for method_name in UI_LAYOUT_METHODS:
            if not hasattr(ui_layout_module, method_name):
                raise NotImplementedError(f"The layout module '{ui_layout}' is missing the required method '{method_name}'.")
    except ModuleNotFoundError as exception:
        logger.error(wording.get('ui_layout_not_loaded').format(ui_layout=ui_layout), __name__)
        logger.debug(exception.msg, __name__)
        hard_exit(1)
    except NotImplementedError as e:
        logger.error(str(e), __name__)
        hard_exit(1)
    return ui_layout_module

def get_ui_layouts_modules(ui_layouts: List[str]) -> List[ModuleType]:
    global UI_LAYOUT_MODULES

    if not UI_LAYOUT_MODULES:
        for ui_layout in ui_layouts:
            ui_layout_module = load_ui_layout_module(ui_layout)
            UI_LAYOUT_MODULES.append(ui_layout_module)
    return UI_LAYOUT_MODULES

def launch() -> None:
    ui_layouts_total = len(state_manager.get_item('ui_layouts'))
    with gradio.Blocks(theme=get_theme(), css=get_css(), title=metadata.get('name') + ' ' + metadata.get('version'), fill_width=True) as ui:
        for ui_layout in state_manager.get_item('ui_layouts'):
            ui_layout_module = load_ui_layout_module(ui_layout)

            if ui_layouts_total > 1:
                with gradio.Tab(ui_layout):
                    ui_layout_module.render()
                    ui_layout_module.listen()
            else:
                ui_layout_module.render()
                ui_layout_module.listen()

    for ui_layout in state_manager.get_item('ui_layouts'):
        ui_layout_module = load_ui_layout_module(ui_layout)
        ui_layout_module.run(ui)

def get_theme() -> gradio.Theme:
    return gradio.themes.Base(
        primary_hue=gradio.themes.colors.red,
        secondary_hue=gradio.themes.colors.neutral,
        radius_size=Size(xxs='0.375rem', xs='0.375rem', sm='0.375rem', md='0.375rem', lg='0.375rem', xl='0.375rem', xxl='0.375rem'),
        font=gradio.themes.GoogleFont('Open Sans')
    ).set(
        # Additional theme properties can be added here...
    )

def get_css() -> str:
    overrides_css_path = resolve_relative_path('uis/assets/overrides.css')
    with open(overrides_css_path, 'r') as f:
        return f.read()
