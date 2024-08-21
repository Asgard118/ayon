from unittest.mock import MagicMock
import pytest
import tempfile
import pygit2
from pathlib import Path
import os
import shutil


@pytest.fixture
def temp_repo():
    temp_dir = tempfile.mkdtemp()
    repo_path = Path(temp_dir) / "repo"
    os.makedirs(repo_path, exist_ok=True)

    repo = pygit2.init_repository(repo_path.as_posix(), bare=False)

    builder = repo.TreeBuilder()
    file_path = repo_path / "example.txt"
    file_content = b"File content"

    with open(file_path, 'wb') as f:
        f.write(file_content)

    blob_id = repo.create_blob_fromdisk(file_path.as_posix())
    builder.insert("example.txt", blob_id, pygit2.GIT_FILEMODE_BLOB)
    tree_id = builder.write()

    author = pygit2.Signature("Tester", "tester@example.com")
    committer = pygit2.Signature("Tester", "tester@example.com")
    commit_id = repo.create_commit(
        "refs/heads/main", author, committer, "Initial commit", tree_id, []
    )

    repo.remotes.create("origin", "https://github.com/Asgard118/py_tests")

    try:
        yield repo, repo_path
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def test_class_instance(temp_repo):
    from ayon_tools.repository import Repository
    repo, repo_path = temp_repo
    instance = Repository()
    instance.repo = MagicMock()
    instance.repo.get = MagicMock()
    instance.workdir = repo_path
    return instance

@pytest.fixture
def test_class_instance_without_mock(temp_repo):
    from ayon_tools.repository import Repository
    repo, repo_path = temp_repo
    instance = Repository()
    instance.repo = repo
    instance.workdir = repo_path
    return instance

#эти три работают, но иногда бывает ошибка, время ожидания истекло. Откуда и почему она еще не понял
def test_read_from_repo_success(test_class_instance_without_mock):
    result = test_class_instance_without_mock.read_from_repo("example.txt", "main", default=None)
    assert result == b"File content"

def test_read_from_repo_branch_not_found(test_class_instance):
    with pytest.raises(ValueError) as excinfo:
        test_class_instance.read_from_repo("example.txt", "non_existing_branch", default=None)
    assert "Branch non_existing_branch not found" in str(excinfo.value)

def test_read_from_repo_file_not_found_with_default(test_class_instance):
    mock_get = test_class_instance.repo.get
    mock_get.return_value.tree = {}
    result = test_class_instance.read_from_repo("non_existing_file.txt", "main", default="default_value")
    assert result == "default_value"

# def test_read_from_repo_file_not_found_no_default(test_class_instance):
#     test_class_instance.repo.get.return_value.tree = {}
#     with pytest.raises(FileNotFoundError) as excinfo:
#         test_class_instance.read_from_repo("test_exsist.txt", "main", default=None)
#     assert "File main:test_exsist.txt not found," in str(excinfo.value)