from ayon_tools.base_addon import Addon
from ayon_tools.repository import repo


class TryPublisherAddon(Addon):


	def solve_shortcuts(self, settings: dict, project: str = None):
		if project:
			app_setting = repo.get_file_contentPath("projects", project, "addons", self.name, "defaults.json").as_posix()
		else:
			app_setting = repo.get_file_content("core.yml", branch=self.studio.name, default=None)
		return app_setting