import pytest
from ayon_tools.studio import StudioSettings
import json
from pathlib import Path
from ayon_tools.commands.backup_restore import dump


@pytest.fixture
def studio_settings_mock(mocker):
	studio_mock = mocker.Mock(spec=StudioSettings)

	studio_mock.get_default_anatomy_preset.return_value = {"preset": "default"}
	studio_mock.get_attributes.return_value = {"attribute_key": "attribute_value"}
	studio_mock.get_staging_bundle.return_value = {"bundle_key": "staging_bundle_value"}
	studio_mock.get_productions_bundle.return_value = {"bundle_key": "production_bundle_value"}
	studio_mock.get_server_addons_settings.return_value = {"addon_key": "addon_value"}

	projects = [{"name": "Project1"}, {"name": "Project2"}]
	studio_mock.get_projects.return_value = projects

	studio_mock.get_project_anatomy.return_value = {"anatomy_key": "anatomy_value"}
	studio_mock.get_project_addons_settings.return_value = {"addon_key": "project_addon_value"}
	studio_mock.get_project_settings_for_status.return_value = {"status_key": "status_value"}

	return studio_mock


def test_dump_creates_file(studio_settings_mock, tmpdir):
	file_path = tmpdir.join("studio_dump.json")
	result_path = dump(studio_settings_mock, path=file_path)
	assert Path(result_path).exists()


def test_dump_correct_data(studio_settings_mock, tmpdir):
	file_path = tmpdir.join("studio_dump.json")
	result_path = dump(studio_settings_mock, path=file_path)
	with open(result_path, "r") as file:
		data = json.load(file)

	assert data["server_anatomy"] == {"preset": "default"}
	assert data["server_attributes"] == {"attribute_key": "attribute_value"}
	assert data["projects"]["Project1"]["anatomy"] == {"anatomy_key": "anatomy_value"}
