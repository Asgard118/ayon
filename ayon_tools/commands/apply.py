from ayon_tools.studio import StudioSettings
from ayon_tools import tools
import json
from ayon_tools.api import system

def run(studio: StudioSettings, project: list[str] = None, **kwargs):
    # CHECK DIFF
    # projects = project or studio.get_all_projects()

    # apply anatomy
    # anatomy = studio.get_rep_anatomy()
    # conv_anatomy = tools.convert_bytes_to_str(anatomy)
    # anatomy_json = json.dumps(conv_anatomy)
    # server_anatomy = studio.get_anatomy()
    # preset_name = studio.get_default_anatomy_name()
    # if tools.compare_dicts(anatomy_json, server_anatomy):
    #     return None
    # else:
    #     studio.set_anatomy(preset_name, anatomy_json)

    # apply attributes
    attributes = studio.get_rep_attributes()
    conv_attributes = tools.convert_bytes_to_str(attributes)
    attributes_json = json.dumps(conv_attributes)
    attributes_json_n = json.loads(attributes_json)
    server_attributes = studio.get_attributes()
    if tools.compare_dicts(attributes_json, server_attributes):
        next()
    else:
        for attribute in attributes_json_n["attributes"]:
            name_attributes = attribute["name"]
            data_conf = {
                "position": attribute["position"],
                "scope": attribute["scope"],
                "builtin": attribute["builtin"],
                "data": attribute["data"]
            }
            attributes.set_attributes(name_attributes, data_conf)


    # apply bundle
    # bundle = studio.get_rep_bundle()
    # conv_bundle = tools.convert_bytes_to_str(bundle)
    # bundle_json = json.dumps(conv_bundle)
    # product_bundles_name = studio.get_productions_bundle()
    # studio_setting_bundle = studio.get_bundles()
    # target_name = product_bundles_name['bundleName']
    # server_bundle = next((bundle for bundle in studio_setting_bundle.get("bundles", []) if bundle.get("name") == target_name), None)
    # if tools.compare_dicts(bundle_json, server_bundle):
    #     return None
    # else:
    #     return studio.update_bundle(bundle_json, target_name)


    # appy studio settings



    # apply projects settings
    # for project in projects:
    #     anatomy = studio.get_actual_anatomy(project)
    #     studio.set_project_anatomy(project, anatomy)
    #     studio.set_project_addon_settings(...)
    # CHECK DIFF
