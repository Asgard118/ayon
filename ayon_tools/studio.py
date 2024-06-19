from .api import anatomy, bundles, attributes, auth, addons
from . import config


class Studio:
	def __init__(self, name: str):
		studio_local_config = config.get_studio_local_config(name)
		self.name = name
		self.auth = auth.Auth(studio_local_config['server_url'], studio_local_config['token'])

	def get_addons_data(self, project_name: str):
		return addons.get_project_settings(project_name)

	def get_addon_data(self, name: str, ver: str):
		return addons.get_addon_studio_settings(name, ver)

	def get_anatomy_data(self, preset_name: str):
		return anatomy.get_studio_anatomy_preset(preset_name)

	def get_attributes_data(self):
		return attributes.get_attributes()

	def get_bundle_data(self, name: str):
		return bundles.get_bundle(name)

	def get_project_anatomy_data(self, project_name: str, url: str, head: str):
		return anatomy.get_project_anatomy(project_name, url, head)