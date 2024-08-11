import sys
from contextlib import contextmanager
from unittest.mock import Mock, MagicMock


def mock_modules(*modules):
	for mod in modules:
		sys.modules[mod] = Mock()

mock_modules('redis', 'nxtools','codenamize', 'orjson', 'asyncpg', 'asyncpg.pool', 'asyncpg.transaction', 'aiocache', 'ayon_server.lib.postgres', 'ayon_server.lib.redis', 'strawberry', 'strawberry.experimental.pydantic', 'ayon_server.entities.core.base',
			 'ayon_server.entities.core', 'ayon_server.helpers.hierarchy_cache', 'ayon_server.entities',
			 'ayon_server.actions', 'ayon_server.actions.context', 'ayon_server.actions.execute', 'ayon_server.actions.manifest', 'ayon_server.settings.anatomy', 'semver',
			 )


def _get_settings(mod):
	for name, obj in mod.__dict__.items():
		if 'DEFAULT' in name and isinstance(obj, dict):
			return obj

def _get_addon_class(mod):
	from ayon_server.addons import BaseServerAddon
	import inspect
	for obj in mod.__dict__.values():
		if inspect.isclass(obj):
			if BaseServerAddon in obj.__bases__:
				return obj

@contextmanager
def _temp_pypath(path):
	try:
		sys.path.append(path)
		yield
	finally:
		sys.path.remove(path)

def get_addon_default_settings(addon_name):
	from .addon_tools import get_addon_repo_path
	path = get_addon_repo_path(addon_name)
	with _temp_pypath(path):
		import server
		settings = _get_settings(server)
		addon_class = _get_addon_class(server)
		settings_model = addon_class.settings_model(**settings)
		return settings_model.dict()

