# from ayon_tools.api import bundles, addons
from ayon_tools.studio import StudioSettings


def process(studio: StudioSettings, project: list[str] = None, **kwargs):

    projects = project or studio.get_all_projects()

    # apply anatomy
    anatomy = studio.get_actual_anatomy()
    ...

    # apply bundle
    bundle = studio.get_actual_bundle()
    ...

    # apply attributes
    attributes = studio.get_actual_attributes()
    ...

    # apply projects settings
    for project in projects:
        anatomy = studio.get_actual_anatomy(project)
        studio.set_project_anatomy(project, anatomy)

        studio.set_project_addon_settings(...)
