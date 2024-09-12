import ayon_api
from .auth import default_auth, Auth
from ayon_tools import tools



# dependency packages
def get_dep_packages(auth: Auth = default_auth) -> dict:
    """
    Возвращает dependency packages на сервере
    """
    with auth:
        data = ayon_api.get_dependency_packages()
    return data


def upload_dep_package(
    archive: str, file_name: str,  auth: Auth = default_auth
):
    with auth:
        ayon_api.upload_dependency_package(archive, file_name)


def create_dep_packages(auth: Auth = default_auth, *args, **kwargs):
    with auth:
        ayon_api.create_dependency_package(*args, **kwargs)

def set_dep_pack(name: str, auth: Auth = default_auth):
    zip = tools.get_dependency(name)
    package_data = tools.get_dependency(name, json=True)
    filename = package_data["filename"]
    with auth:
        create_dep_packages(**package_data)
        upload_dep_package(zip, filename)