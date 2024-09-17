import json

from ayon_tools.base_addon import Addon
from ayon_tools.repository import repo


class CoreAddon(Addon):

    def solve_shortcuts(self, settings: dict, project: str = None):
        # if project:
        # 	app_setting = repo.get_file_contentPath("projects", project, "addons", self.name, "defaults.json").as_posix()
        # else:
        app_setting = repo.get_file_content(
            "project.yml", branch=self.studio.name, default=None
        )
        if app_setting:
            envs = app_setting.get("envs")
            if envs:
                current_envs = json.loads(settings.get("project_environments", "{}"))
                settings["project_environments"] = json.dumps(
                    {**current_envs, **envs}, indent=2
                )
        return settings
