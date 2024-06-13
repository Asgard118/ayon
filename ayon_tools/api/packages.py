from ayon_api import get_dependency_packages, upload_dependency_package
# dependency packages
def get_dep_packages() -> dict:
	"""
	Возвращает dependency packages на сервере
	"""
	data = get_dependency_packages()
	return data

def upload_dep_package(archive: str, file_name: str, platform_name: str):
	upload_dependency_package(archive, file_name, platform_name)


