from ayon_tools.studio import StudioSettings

def get_addon_repo_path(addon: str, studio: StudioSettings, addon_ver: str):
    from ayon_tools.repository import Repository
    addon = studio.get_addon(addon)
    addon_url = addon.get_repository_url()
    addon_repo = Repository(addon_url)
    addon_repo.reload()
    addon_repo.set_tag(addon_ver)
    return addon_repo.workdir.as_posix()