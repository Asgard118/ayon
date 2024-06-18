import ayon_api
from ayon_api import get_bundle_settings
import os

class BundleMode:
    PRODUCTION = 'production'
    STAGING = 'staging'

# bundles
def get_bundles() -> dict:
    return ayon_api.get_bundles()

def get_bundle(bundle_name: str) -> dict:
    """
    Возвращает аддоны бандла по имени бандла
    # example
    {
        {'aftereffects': '0.1.3',
         'applications': '0.1.4',
         'blender': '0.1.6',
         'houdini': '0.2.11',
         'max': '0.1.5',
         'maya': '0.1.8',
        }
    }
        """
    data = get_bundles()
    if 'bundles' in data:
        for bundle in data['bundles']:
            if bundle['name'] == bundle_name:
                return bundle['addons']

def get_production_bundle() -> dict:
    """
    Функция возвращает настройки бандла в статусе production
    """
    data = get_bundle_settings()
    return data

def get_staging_bundle() -> dict:
    """
    Возвращает бандл в статусе staging
    """
    data = get_bundles().get('bundles', [])
    return next((item for item in data if item.get('isStaging')), None)

def create_bundle(
        name: str,
        addons: dict,
        installer_version: str,
        dependency_packages=None):
    """
    Создает бандл, с указаным названием, аддонами и их версиями, и версией инсталера
    """
    ayon_api.create_bundle(
        name=name,
        addon_versions=addons,
        installer_version=installer_version,
        dependency_packages=dependency_packages)
