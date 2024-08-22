from unittest.mock import MagicMock
import pytest
import tempfile
import pygit2
from pathlib import Path
import os
import shutil
import json
import yaml


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


#test read from repo
# def test_read_from_repo_success(test_class_instance_without_mock):
#     result = test_class_instance_without_mock.read_from_repo("example.txt", "main", default=None)
#     assert result == b"File content"
#
# def test_read_from_repo_branch_not_found(test_class_instance):
#     with pytest.raises(ValueError) as excinfo:
#         test_class_instance.read_from_repo("example.txt", "non_existing_branch", default=None)
#     assert "Branch non_existing_branch not found" in str(excinfo.value)
#
# def test_read_from_repo_file_not_found_with_default(test_class_instance):
#     mock_get = test_class_instance.repo.get
#     mock_get.return_value.tree = {}
#     result = test_class_instance.read_from_repo("non_existing_file.txt", "main", default=None)
#     assert result == None
#
# #test get file content
# def test_get_file_content_json(test_class_instance_without_mock):
#     json_data = {"key": "value"}
#     json_file_path = test_class_instance_without_mock.workdir / "test.json"
#
#     with open(json_file_path, "w") as f:
#         json.dump(json_data, f)
#
#     repo = test_class_instance_without_mock.repo
#     builder = repo.TreeBuilder()
#     blob_id = repo.create_blob_fromdisk(json_file_path.as_posix())
#     builder.insert("test.json", blob_id, pygit2.GIT_FILEMODE_BLOB)
#     tree_id = builder.write()
#
#     author = pygit2.Signature("Tester", "tester@example.com")
#     committer = pygit2.Signature("Tester", "tester@example.com")
#
#     parent_commit = repo.head.peel(pygit2.Commit)
#
#     repo.create_commit("refs/heads/main", author, committer, "Add test.json", tree_id, [parent_commit.id])
#
#     result = test_class_instance_without_mock.get_file_content("test.json", branch="main")
#     assert result == json_data
#
# def test_get_file_content_yaml(test_class_instance_without_mock):
#     yaml_data = {"key": "value"}
#     yaml_file_path = test_class_instance_without_mock.workdir / "test.yaml"
#
#     with open(yaml_file_path, "w") as f:
#         yaml.dump(yaml_data, f)
#
#     repo = test_class_instance_without_mock.repo
#     builder = repo.TreeBuilder()
#     blob_id = repo.create_blob_fromdisk(yaml_file_path.as_posix())
#     builder.insert("test.yaml", blob_id, pygit2.GIT_FILEMODE_BLOB)
#     tree_id = builder.write()
#
#     author = pygit2.Signature("Tester", "tester@example.com")
#     committer = pygit2.Signature("Tester", "tester@example.com")
#
#     parent_commit = repo.head.peel(pygit2.Commit)
#
#     repo.create_commit("refs/heads/main", author, committer, "Add test.json", tree_id, [parent_commit.id])
#
#     result = test_class_instance_without_mock.get_file_content("test.yaml", branch="main")
#     assert result == yaml_data
#
# def test_get_file_content_from_current_files(test_class_instance_without_mock):
#     test_class_instance_without_mock.read_from_current_files = True
#     local_file_path = test_class_instance_without_mock.workdir / "local_file.txt"
#     file_content = "Local file content"
#     with open(local_file_path, "w") as f:
#         f.write(file_content)
#
#     result = test_class_instance_without_mock.get_file_content("local_file.txt")
#     assert result == file_content




#test read from file
def test_read_from_file_success(test_class_instance_without_mock):
    file_name = "test_file.txt"
    file_content = "Test content"
    file_path = Path(test_class_instance_without_mock.workdir) / file_name
    with open(file_path, 'w') as f:
        f.write(file_content)

    result = test_class_instance_without_mock.read_from_file(file_name, default=None)
    assert result == file_content


def test_read_from_file_default_value(test_class_instance_without_mock):
    result = test_class_instance_without_mock.read_from_file("non_existing_file.txt", default="default_value")
    assert result == "default_value"


def test_read_from_file_file_not_found(test_class_instance_without_mock):
    result = test_class_instance_without_mock.read_from_file("non_existing_file.txt", default=None)
    assert result == None