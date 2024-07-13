from pathlib import Path
from pprint import pprint

from ayon_tools.base_shortcut_solver import Solver
from ayon_tools.repository import repo
from ayon_tools.tools import merge_dicts


class AnatomySolver(Solver):
    def solve(self, project_name: str = None):
        default_anatomy = self.get_default_anatomy(project_name)
        anatomy_data = self.resolve_shortcuts(default_anatomy, project_name)
        return anatomy_data

    def get_default_anatomy(self, project_name: str = None) -> dict:
        default_anatomy = repo.get_file_content("defaults/anatomy.json")
        if project_name:
            project_default_anatomy = repo.get_file_content(
                Path("projects", project_name, "anatomy.json").as_posix(), default=None
            )
            if project_default_anatomy:
                return merge_dicts(default_anatomy, project_default_anatomy)
        return default_anatomy

    def resolve_shortcuts(self, default_data, project_name=""):
        # templates
        self.resolve_templates(default_data, project_name)
        self.resolve_folders(default_data, project_name)
        self.resolve_tasks(default_data, project_name)
        self.resolve_attributes(default_data, project_name)
        return default_data

    def resolve_templates(self, data: dict, project_name: str = None):
        project_data = (
            repo.get_file_content(
                Path(project_name, "templates.yml").as_posix(), default={}
            )
            if project_name
            else {}
        )
        studio_data = repo.get_file_content("templates.yml", default={})
        # roots
        repo_roots = studio_data.get("roots", {}) | project_data.get("roots", {})
        roots = []
        for root_name, root_data in repo_roots.items():
            roots.append(dict(name=root_name, **root_data))
            # merge roots
        data["roots"] = roots
        # templates
        studio_templates = studio_data.get("templates", {})
        project_templates = project_data.get("templates", {})
        template_types = set(studio_templates.keys()) | set(project_templates.keys())
        templates_data = {}
        for template_type in template_types:
            templates_data.setdefault(template_type, [])
            for tmpl_data in (studio_templates, project_templates):
                for template_name, template_data in tmpl_data.get(
                    template_type, {}
                ).items():
                    templates_data[template_type].append(
                        dict(name=template_name, **template_data)
                    )
        data["templates"] = templates_data
        # template variables
        variables = studio_data.get("variables", {}) | project_data.get("variables", {})
        if variables:
            data.setdefault("templates", {})
            data["templates"].update(variables)

    def resolve_folders(self, data: dict, project_name: str = None):
        folders = (
            repo.get_file_content(
                Path("projects", project_name, "folders.yml").as_posix(), default={}
            )
            if project_name
            else {}
        ) or repo.get_file_content("folders.yml", default={})
        if folders:
            for folder in folders:
                folder.setdefault("icon", "")
                folder.setdefault("original_name", folder["name"])
            data["folder_types"] = folders
        return data

    def resolve_tasks(self, data: dict, project_name: str = None):
        studio_tasks_data = repo.get_file_content("tasks.yml", default={})
        project_tasks_data = (
            repo.get_file_content(
                Path("projects", project_name, "tasks.yml").as_posix(), default={}
            )
            if project_name
            else {}
        )
        # task types
        tasks_types_list = project_tasks_data.get(
            "task_types"
        ) or studio_tasks_data.get("task_types")
        fixed_tasks = []
        for task in tasks_types_list:
            task.setdefault("icon", "")
            task.setdefault("original_name", task["name"])
            fixed_tasks.append(task)
        if fixed_tasks:
            data["task_types"] = fixed_tasks
        # task statuses
        statuses_data = project_tasks_data.get("statuses") or studio_tasks_data.get(
            "statuses"
        )
        if statuses_data:
            for status_type in statuses_data:
                status_type.setdefault("color", "#FFF")
                status_type.setdefault("icon", "")
                status_type.setdefault("original_name", status_type["name"])
            data["statuses"] = statuses_data
        return data

    def resolve_attributes(self, data: dict, project_name: str = None):
        # project settings
        ...
        # applications
        ...
        pass
