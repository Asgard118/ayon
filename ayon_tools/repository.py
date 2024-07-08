import logging
import json
from pathlib import Path
import yaml
import pygit2

from . import config

NONETYPE = type("NoneType")


class Repository:
    default_branch = "main"

    def __init__(self):
        self.url = config.REPOSITORY_URL
        self.workdir = config.REPOSITORY_DIR
        self._git_repo: pygit2.Repository or None = None

    @property
    def repo(self):
        if self._git_repo is None:
            self.reload()
        return self._git_repo

    def reload(self):
        if not self.workdir.exists() or not list(self.workdir.iterdir()):
            # clone if not exists
            logging.info(f"Cloning repository from {self.url} to {self.workdir}")
            self._git_repo = pygit2.clone_repository(self.url, self.workdir.as_posix())
        else:
            logging.info(f"Updating repository in {self.workdir}")
            # update all if exists
            repo = pygit2.Repository(self.workdir / ".git")
            repo.reset(repo.head.target, pygit2.GIT_RESET_HARD)
            remote = repo.remotes["origin"]
            remote.fetch()
            for branch in repo.branches:
                if branch.startswith("refs/remotes/origin/"):
                    local_branch = branch.replace("refs/remotes/origin/", "refs/heads/")
                    if local_branch in repo.branches:
                        repo.checkout(local_branch)
                        repo.merge(repo.get(branch))
            self._git_repo = repo

    def set_branch(self, branch_name: str):
        # check current branch
        current = self.repo.head.shorthand
        if current != branch_name:
            if branch_name not in self.repo.branches:
                raise NameError(f"Branch {branch_name} not found in repository")
            self.repo.reset(self.repo.head.target, pygit2.GIT_RESET_HARD)
            # force switch if not match
            self.repo.checkout(self.repo.branches[branch_name])
            logging.info(f"Switched to branch {branch_name}")
        else:
            logging.info(f"Already on branch {branch_name}")

    def get_file_content(self, file_name: str, branch: str = None, default=NONETYPE):
        """
        Get file content from the latest commit of the specified branch
        """
        branch = branch or self.default_branch
        logging.debug(f"Getting file content {file_name} from {branch}")
        branch_ref = f"refs/remotes/origin/{branch}"
        if branch_ref not in self.repo.references:
            raise ValueError(f"Branch {branch} not found")
        branch_commit = self.repo.lookup_reference(branch_ref).target
        commit = self.repo.get(branch_commit)
        tree = commit.tree
        try:
            entry = tree[file_name]
        except KeyError:
            if default is not NONETYPE:
                return default
            raise FileNotFoundError(
                f"File {file_name} not found in branch {branch}, {self.workdir}"
            )
        file_blob = self.repo[entry.id]
        data = file_blob.data
        if Path(file_name).suffix == ".json":
            logging.debug("Decoding JSON")
            data = json.loads(data)
        elif Path(file_name).suffix in (".yaml", ".yml"):
            logging.debug("Decoding YAML")
            data = yaml.safe_load(data)
        return data


repo = Repository()
