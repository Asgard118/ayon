import ayon_api


# dependency packages
def get_dep_packages() -> dict:
    """
    Возвращает dependency packages на сервере
    """
    data = ayon_api.get_dependency_packages()
    return data


def upload_dep_package(archive: str, file_name: str):
    ayon_api.upload_dependency_package(archive, file_name)
