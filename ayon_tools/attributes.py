from ayon_api import get_attributes_schema, set_attribute_config
def get_attributes() -> dict:
    """
    Функция возвращает список атрибутов
    """
    data = get_attributes_schema()
    return data
def set_attributes(attributes: dict):
    """
    Функцию добавили в АПИ 8 числа, еще не понятно как она работает
    """
    set_attribute_config()

def create_attribute(name: str, attr_type: str):
    attributes = get_attributes()
    ...
    set_attributes(attributes)
