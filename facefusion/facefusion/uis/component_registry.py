# facefusion/uis/component_registry.py
from typing import Dict, Optional
from facefusion.uis.typing import Component, ComponentName

UI_COMPONENTS: Dict[ComponentName, Component] = {}

def get_ui_component(component_name: ComponentName) -> Optional[Component]:
    """Fetches a UI component by name from the registered components."""
    return UI_COMPONENTS.get(component_name)

def register_ui_component(component_name: ComponentName, component: Component) -> None:
    """Registers a UI component by its name."""
    UI_COMPONENTS[component_name] = component
