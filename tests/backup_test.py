import pytest
import json
from pathlib import Path
from ayon_tools.studio import StudioSettings
from ayon_tools.commands.backup_restore import dump


@pytest.fixture
def real_studio_settings():
	studio = StudioSettings("main")
	return studio


def test_dump_real_data(real_studio_settings):
	test_path = "/tmp/test_output_real.json"
	result_path = dump(real_studio_settings, test_path)

	assert result_path == test_path

	assert Path(test_path).exists()

	with open(test_path, "r") as file:
		data = json.load(file)

	assert "server_anatomy" in data
	assert "server_attributes" in data
	assert "projects" in data



def test_dump_real_data_auto_path(real_studio_settings):
	result_path = dump(real_studio_settings)
	assert Path(result_path).exists()

	with open(result_path, "r") as file:
		data = json.load(file)

	assert "server_anatomy" in data
	assert "server_attributes" in data
	assert "projects" in data
