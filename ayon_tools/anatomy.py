# studio presets
def get_studio_anatomy_presets_names() -> list: ...
def get_studio_anatomy_preset(preset_name: str) -> dict: ...
def set_studio_anatomy_preset(preset_name: str, preset: dict): ...
def create_studio_anatomy_preset(preset_name: str, preset: dict): ...


# project anatomy
def get_project_anatomy(project_name: str) -> dict: ...
def set_project_anatomy(project_name: str, anatomy: dict): ...

