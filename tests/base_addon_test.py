import pytest
from ayon_tools.studio import StudioSettings
from ayon_tools.base_addon import Addon

test_addon = 'maya'

@pytest.fixture
def real_studio_settings():
    return StudioSettings("main")

@pytest.fixture
def real_addon_instance(real_studio_settings):
    return Addon(test_addon, real_studio_settings)


def test_get_server_settings_real(real_addon_instance):
    result = real_addon_instance.get_server_settings("0.1.18")

    assert isinstance(result, dict)

def test_get_addon_info_real(real_addon_instance):
    info = real_addon_instance.get_addon_info()

    assert isinstance(info, dict)
    assert info["name"] == real_addon_instance.name


def test_get_default_settings_real(real_addon_instance):
    result = real_addon_instance.get_default_settings("0.2.10")

    assert isinstance(result, dict)

def test_get_custom_attributes_real(real_addon_instance):
    attributes = real_addon_instance.get_custom_attributes()

    assert isinstance(attributes, list)

def test_get_addon_class_real(real_studio_settings):
    addon_class = Addon.get_addon_class(test_addon, real_studio_settings)

    assert issubclass(addon_class, Addon)


def test_get_repository_url_real(real_addon_instance):
    url = real_addon_instance.get_repository_url()

    assert isinstance(url, str)
    assert url.startswith("http")
