import pytest
import json
from pathlib import Path
from ayon_tools.studio import StudioSettings
from ayon_tools.commands.backup_restore import dump

# STUDIO_NAME = "main"
#
# @pytest.fixture
# def studio():
# 	return StudioSettings(STUDIO_NAME)
#
#
# def test_dump_initial_setup(studio, tmp_path):
# 	projects = studio.get_projects()
# 	path = tmp_path / "test_dump.json"
# 	result = dump(studio, str(path))
# 	assert result == str(path)
# 	assert path.exists()
# 	assert path.parent.exists()
#
# 	with open(path, "r") as f:
# 		data = json.load(f)
#
# 	expected_keys = [
# 		"server_anatomy",
# 		"server_attributes",
# 		"server_staging_bundle",
# 		"server_production_bundle",
# 		"server_addons",
# 		"projects"
# 	]
# 	for key in expected_keys:
# 		assert key in data, f"Expected key '{key}' not found in data"
#
# 	assert isinstance(data["server_anatomy"], dict)
# 	assert isinstance(data["server_attributes"], dict)
# 	assert isinstance(data["server_staging_bundle"], dict)
# 	assert isinstance(data["server_production_bundle"], dict)
# 	assert isinstance(data["server_addons"], dict)
# 	assert isinstance(data["projects"], dict)
#
# 	for project in projects:
# 		assert project["name"] in data["projects"], f"Project {project['name']} not found in dumped data"
#
# 	result = dump(studio)
# 	assert Path(result).exists()
# 	assert result.endswith(".json")
#
# 	string_result = dump(studio, str(tmp_path / "string_test.json"))
# 	assert Path(string_result).exists()
#
# 	with open(string_result, "r") as f:
# 		string_data = json.load(f)
#
# 	for key in expected_keys:
# 		assert key in string_data, f"Expected key '{key}' not found in data when using string input"
#
# 	deep_path = tmp_path / "subdir1" / "subdir2" / "test_dump.json"
# 	result = dump(studio, str(deep_path))
# 	assert deep_path.parent.exists()
# 	assert deep_path.exists()
#
# 	kwargs_result = dump(studio, str(tmp_path / "kwargs_test.json"), some_kwarg="test_value")
# 	assert Path(kwargs_result).exists()
#
#
# def test_dump_data_consistency(studio, tmp_path):
# 	path1 = tmp_path / "dump1.json"
# 	path2 = tmp_path / "dump2.json"
#
# 	dump(studio, str(path1))
# 	dump(studio, str(path2))
#
# 	with open(path1, "r") as f1, open(path2, "r") as f2:
# 		data1 = json.load(f1)
# 		data2 = json.load(f2)
#
# 	assert data1 == data2, "Data inconsistency between two dumps"
#
#
# def test_project_data_structure(studio, tmp_path):
# 	path = tmp_path / "project_test.json"
# 	dump(studio, str(path))
#
# 	with open(path, "r") as f:
# 		data = json.load(f)
#
# 	assert "projects" in data
# 	for project_name, project_data in data["projects"].items():
# 		assert "anatomy" in project_data
# 		assert "settings" in project_data
# 		assert "projects_settings_staging" in project_data
# 		assert "projects_settings_production" in project_data