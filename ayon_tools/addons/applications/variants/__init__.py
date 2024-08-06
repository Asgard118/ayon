from pathlib import Path
from importlib import import_module
from .base import AppVariant


def get_variant_class(name):
    base_name = __name__
    for mod in Path(__file__).parent.iterdir():
        if mod.stem.startswith("_") or mod.stem == "base":
            continue
        module = import_module(f"{base_name}.{mod.stem}")
        for obj in vars(module).values():
            if (
                isinstance(obj, type)
                and issubclass(obj, AppVariant)
                and obj != AppVariant
            ):
                if obj.app_name == name:
                    return obj
