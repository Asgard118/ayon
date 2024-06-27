import logging
import json
from pathlib import Path

import pygit2

from . import config


class Repository:
    default_branch = "main"

    def __init__(self):
        self.url = config.REPOSITORY_URL
        self.workdir = config.REPOSITORY_DIR
        self._git_repo: pygit2.Repository | None = None

    @property
    def repo(self):
        if not self._git_repo:
            self._git_repo = self.reload()
        return self._git_repo

    def reload(self):
        if not self.workdir.exists() or not list(self.workdir.iterdir()):
            # clone if not exists
            return pygit2.clone_repository(self.url, self.workdir.as_posix())
        else:
            # update all if exists
            repo = pygit2.Repository(self.workdir / ".git")
            repo.reset(repo.head.target, pygit2.GIT_RESET_HARD)
            remote = repo.remotes["origin"]
            remote.fetch()
            return repo

    def set_branch(self, branch_name: str):
        # check current branch
        current = self.repo.head.shorthand
        if current != branch_name:
            if branch_name not in self.repo.branches:
                raise NameError(f"Branch {branch_name} not found in repository")
            self.repo.reset(self.repo.head.target, pygit2.GIT_RESET_HARD)
            # force switch if not match
            self.repo.checkout(self.repo.branches[branch_name])
            logging.debug(f"Switched to branch {branch_name}")
        else:
            logging.debug(f"Already on branch {branch_name}")

    def get_file_content(self, file_name: str, branch: str = None):
        """
        Get file content from branch
        """
        branch = branch or self.default_branch
        branch_ref = f"refs/heads/{branch}"
        if branch_ref not in self.repo.references:
            branch_ref = f"refs/remotes/origin/{branch}"
            if branch_ref not in self.repo.references:
                raise ValueError(f"Branch {branch} not found")
        branch_commit = self.repo.lookup_reference(branch_ref).peel(pygit2.Commit)
        tree = branch_commit.tree
        try:
            entry = tree[file_name]
        except KeyError:
            raise FileNotFoundError(f"File {file_name} not found in branch {branch}")
        file_blob = self.repo[entry.id]
        data = file_blob.data
        if Path(file_name).suffix == ".json":
            data = json.loads(data)
        # TODO: yaml/yml
        return data


repo = Repository()
