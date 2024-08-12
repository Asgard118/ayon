import logging
import json
from pathlib import Path
import yaml
import pygit2

from . import config

NOT_SET_TYPE = type("NoneType")


class Repository:
    default_branch = "main"
    skip_update = False
    read_from_current_files = False

    def __init__(self, url: str = None):
        self.url = url or config.REPOSITORY_URL
        self.repo_name = Path(self.url).stem
        self.workdir = config.REPOSITORY_DIR.joinpath(self.repo_name)
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
            self._git_repo = pygit2.Repository(self.workdir / ".git")
            if self.skip_update:
                logging.info("Skip updating repository")
                return
            logging.info(f"Updating repository in {self.workdir}")
            # update all if exists
            self._git_repo.reset(self._git_repo.head.target, pygit2.GIT_RESET_HARD)
            remote = self._git_repo.remotes["origin"]
            remote.fetch()
            for branch in self._git_repo.branches:
                if branch.startswith("refs/remotes/origin/"):
                    local_branch = branch.replace("refs/remotes/origin/", "refs/heads/")
                    if local_branch in self._git_repo.branches:
                        self._git_repo.checkout(local_branch)
                        self._git_repo.merge(self._git_repo.get(branch))

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

    def set_tag(self, tag_name: str):
        try:
            commit = self.repo.lookup_reference(f"refs/tags/{tag_name}").peel(
                pygit2.Commit
            )
        except KeyError as e:
            raise ValueError(f"Tag '{tag_name}' not found in {self.workdir}") from e
        self.repo.checkout_tree(commit, strategy=pygit2.GIT_CHECKOUT_FORCE)
        self.repo.head.set_target(commit.id)
        return commit.id

    def get_file_content(
        self, file_name: str, branch: str = None, default=NOT_SET_TYPE
    ):
        """
        Get file content from the latest commit of the specified branch
        """
        branch = branch or self.default_branch
        logging.debug(f"Getting file {branch}:{file_name}")
        if self.read_from_current_files:
            if not self.workdir.exists():
                self.reload()
            data = self.read_from_file(file_name, default)
        else:
            data = self.read_from_repo(file_name, branch, default)
        if Path(file_name).suffix == ".json":
            logging.debug("Decoding JSON")
            data = json.loads(data)
        elif data and Path(file_name).suffix in (".yaml", ".yml"):
            logging.debug("Decoding YAML")
            data = yaml.safe_load(data)
        return data

    def read_from_repo(self, file_name, branch, default):
        """
        Чтение файла из данных репозитория. Стандартный способ чтения.
        """
        branch_ref = f"refs/remotes/origin/{branch}"
        if branch_ref not in self.repo.references:
            raise ValueError(f"Branch {branch} not found")
        branch_commit = self.repo.lookup_reference(branch_ref).target
        commit = self.repo.get(branch_commit)
        tree = commit.tree
        try:
            entry = tree[file_name]
        except KeyError:
            if default is not NOT_SET_TYPE:
                return default
            raise FileNotFoundError(
                f"File {branch}:{file_name} not found, {self.workdir}"
            )
        file_blob = self.repo[entry.id]
        data = file_blob.data
        return data

    def read_from_file(self, filename, default):
        """
        Чтение файлов из текущего активного состояния.
        Режим разработки, не учитывает имя ветки.
        """
        file_path = Path(self.workdir) / filename
        if not file_path.exists():
            if default is not NOT_SET_TYPE:
                return default
            raise FileNotFoundError(f"File {file_path} not found")
        with open(file_path, "r") as f:
            data = f.read()
        return data


repo = Repository()
