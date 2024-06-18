import ayon_api
from ayon_api import get_addons_studio_settings, get_addon_studio_settings
from .anatomy import get_studio_anatomy_preset, get_project_anatomy
from attributes import get_attributes
from bundles import get_bundle

class StudioData():

	def __int__(self, name):
		studio_local_config = get_studio_local_config(name)
		self.auth = Auth(studio_local_config['server_url'], studio_local_config['token'])

	def get_addons_data(self):
		data = get_addons_studio_settings()
		return data

	def get_addon_data(self, name: str, ver: str):
		data = get_addon_studio_settings(name, ver)
		return data

	def get_anatomy_data(self, preset_name: str):
		data = get_studio_anatomy_preset(preset_name)
		return data

	def get_attributes_data(self):
		data = get_attributes()
		return data

	def get_bundle_data(self, name: str):
		data = get_bundle(name)
		return data

	def get_project_anatomy_data(self, project_name):
		data = get_project_anatomy(project_name)
		return data