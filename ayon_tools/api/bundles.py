import ayon_api
from ayon_api import get_bundle_settings


class BundleMode:
    PRODUCTION = 'production'
    STAGING = 'staging'


# bundles
def get_bundles() -> dict:
    """
    Example:

    {
    'bundles':
      [
       {
         'addonDevelopment': {},
         'addons': {'aftereffects': '0.1.3',
                    'applications': '0.1.5',
                    'core': '0.1.5',
                    'traypublisher': '0.1.4'
                    ...
                   },
         'createdAt': '2024-06-10T10:37:08.619950+00:00',
         'dependencyPackages': {'darwin': 'ayon_2401161815_darwin.zip',
                                'linux': 'ayon_2310271555_linux.zip',
                                'windows': 'ayon_2310271602_windows.zip'},
         'installerVersion': '1.0.2',
         'isArchived': False,
         'isDev': False,
         'isProduction': True,
         'isStaging': True,
         'name': 'bundle_name'
       },
         ...
      ],
    'devBundles': [],
    'productionBundle': 'bundle_name',
    'stagingBundle': 'staging_bundle_name'
    }"""
    return ayon_api.get_bundles()


def get_bundle(bundle_name: str) -> dict:
    """
    Возвращает аддоны бандла по имени бандла
    {
        {
        'aftereffects': '0.1.3',
        'applications': '0.1.4',
        'blender': '0.1.6',
        ...
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
