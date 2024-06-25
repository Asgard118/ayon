# from ayon_tools.api import bundles, addons
from ayon_tools.studio import StudioSettings


def run(studio: StudioSettings, project: list[str] = None, **kwargs):
    # CHECK DIFF
    # projects = project or studio.get_all_projects()

    # apply anatomy
    anatomy = studio.get_rep_anatomy()
    server_anatomy = studio.get_anatomy()
    # compare ...
    studio.set_default_anatomy(anatomy)

    # apply attributes
    attributes = studio.get_actual_attributes()
    ...

    # apply bundle
    bundle = studio.get_actual_bundle()
    ...

    ...

    # appy studio settings

    # apply projects settings
    for project in projects:
        anatomy = studio.get_actual_anatomy(project)
        studio.set_project_anatomy(project, anatomy)
        studio.set_project_addon_settings(...)
    # CHECK DIFF
