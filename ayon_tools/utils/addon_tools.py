import pygit2
from ayon_tools.repository import Repository, repo
from ayon_tools import exceptipns

def get_addon_repo_path(addon_name: str):
    pa = repo.read_from_repo(f'addons/{addon_name}/info.yml', "main", type("NoneType"))
    print(pa)
    # repo_path = repo.get_file_content(f'addons/{addon_name}/info.yml')
    # url = repo_path.get('url')
    return pa

def build():
    ...

def clone(addon_name: str):
    repo_path = get_addon_repo_path(addon_name)
    # url = repo_path.get('url')
    # new_repo = Repository(url)

clone('maya')