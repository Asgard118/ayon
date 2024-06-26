from ayon_tools.studio import StudioSettings
from ayon_tools import tools
import json


def run(studio: StudioSettings, project: list[str] = None, **kwargs):
    # CHECK DIFF
    # projects = project or studio.get_all_projects()

    # apply anatomy
    repo_anatomy = studio.get_rep_anatomy()
    server_anatomy = studio.get_anatomy()
    preset_name = studio.get_default_anatomy_name()
    if not tools.compare_dicts(repo_anatomy, server_anatomy):
        studio.set_anatomy(preset_name, repo_anatomy)

    # apply attributes
    attributes = studio.get_rep_attributes()
    conv_attributes = tools.convert_bytes_to_str(attributes)
    attributes_json = json.dumps(conv_attributes)
    server_attributes = studio.get_attributes()
    if tools.compare_dicts(attributes_json, server_attributes):
        return None
    else:
        ...

    # apply bundle
    bundle = studio.get_rep_bundle()
    conv_bundle = tools.convert_bytes_to_str(bundle)
    bundle_json = json.dumps(conv_bundle)
    product_bundles_name = studio.get_productions_bundle()
    studio_setting_bundle = studio.get_bundles()
    target_name = product_bundles_name["bundleName"]
    server_bundle = next(
        (
            bundle
            for bundle in studio_setting_bundle.get("bundles", [])
            if bundle.get("name") == target_name
        ),
        None,
    )
    if tools.compare_dicts(bundle_json, server_bundle):
        return None
    else:
        return studio.update_bundle(bundle_json, target_name)

    # appy studio settings

    # apply projects settings
    # for project in projects:
    #     anatomy = studio.get_actual_anatomy(project)
    #     studio.set_project_anatomy(project, anatomy)
    #     studio.set_project_addon_settings(...)
    # CHECK DIFF
