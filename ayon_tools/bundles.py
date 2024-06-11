from ayon_api import get_bundle_settings
import ayon_api
import json
class BundleMode:
    PRODUCTION = 'production'
    STAGING = 'staging'

# bundles
def get_bundles() -> dict:
    return ayon_api.get_bundles()

def get_bundle(bundle_name: str) -> dict:
        """
        Возвращает аддоны бандла по имени бандла
        {
            TODO: пример по запросу на имя имя бандла "bundle-01", вернет:
{'aftereffects': '0.1.3',
 'applications': '0.1.4',
 'blender': '0.1.6',
 'celaction': '0.1.0',
 'clockify': '0.1.1',
 'core': '0.1.5',
 'deadline': '0.1.8',
 'equalizer': '0.0.1',
 'fusion': '0.1.4',
 'hiero': '0.1.2',
 'houdini': '0.2.11',
 'max': '0.1.5',
 'maya': '0.1.8',
 'nuke': '0.1.9',
 'openpype': '3.18.11-nightly.6',
 'photoshop': '0.1.1',
 'resolve': '0.1.0',
 'royalrender': '0.1.1',
 'substancepainter': '0.1.1',
 'timers_manager': '0.1.1',
 'traypublisher': '0.1.3',
 'tvpaint': '0.1.1',
 'unreal': '0.1.0'}
        }
        """
        data = get_bundles()
        if 'bundles' in data:
            for bundle in data['bundles']:
                if bundle['name'] == bundle_name:
                    return bundle['addons']
        return None
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
        dependency_packages=dependency_packages
        )

