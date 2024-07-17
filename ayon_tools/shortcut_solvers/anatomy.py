from pathlib import Path
from ayon_tools.base_shortcut_solver import Solver
from ayon_tools.repository import repo


class AnatomySolver(Solver):
    def solve(self, project_name: str = None):
        default_anatomy = self.get_default_anatomy()
        anatomy_data = self.resolve_shortcuts(default_anatomy, project_name)
        return anatomy_data

    def get_default_anatomy(self):
        return repo.get_file_content("defaults/anatomy.json", branch=self.studio.name)

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
            root_data["darwin"] = root_data.pop("macos", root_data.pop("darwin", ""))
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
        for other_template in ("delivery", "staging", "others"):
            data["templates"].setdefault(other_template, [])
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
                folder.setdefault("shortName", folder.pop("short_name"))
            data["folder_types"] = folders
        return data

    def resolve_tasks(self, data: dict, project_name: str = None):
        # task types
        studio_tasks_data = repo.get_file_content("tasks.yml", default={})
        project_tasks_data = (
            repo.get_file_content(
                Path("projects", project_name, "tasks.yml").as_posix(), default={}
            )
            if project_name
            else {}
        )
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
        # studio default settings
        studio_attrs = repo.get_file_content("project-settings.yml", default={})

        # project settings
        if project_name:
            project_attrs = (
                repo.get_file_content(
                    Path("projects", project_name, "project-settings.yml").as_posix(),
                    default={},
                )
                if project_name
                else {}
            )
            studio_attrs = studio_attrs | project_attrs

        resolution: str | None = studio_attrs.pop("resolution", None)
        if resolution:
            h, w = resolution.split("x")
            studio_attrs["resolutionWidth"], studio_attrs["resolutionHeight"] = int(
                h
            ), int(w)

        for key in ["startDate", "endDate", "description"]:
            if key in studio_attrs:
                del studio_attrs[key]
        # applications
        app_addon = self.studio.get_addon("applications")
        app_list = app_addon.get_app_list_attributes()
        data["attributes"]["applications"] = app_list
        # apply attrs
        data["attributes"].update(studio_attrs)

        # fix types
        data["attributes"]["fps"] = float(data["attributes"]["fps"])
