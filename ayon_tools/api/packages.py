import ayon_api
from .auth import default_auth, Auth


# dependency packages
def get_dep_packages(auth: Auth = default_auth) -> dict:
    """
    Возвращает dependency packages на сервере
    """
    with auth:
        data = ayon_api.get_dependency_packages()
    return data


def upload_dep_package(
    archive: str, file_name: str, platform_name: str, auth: Auth = default_auth
):
    with auth:
        ayon_api.upload_dependency_package(archive, file_name, platform_name)
