
# attributes
def get_attributes() -> dict: ...
def set_attributes(attributes: dict): ...


def create_attribute(name: str, attr_type: str):
    attributes = get_attributes()
    ...
    set_attributes(attributes)

