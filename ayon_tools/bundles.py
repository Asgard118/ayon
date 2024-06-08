
class BundleMode:
    PRODUCTION = 'production'
    STAGING = 'staging'

# bundles
def get_bundles(archived=False) -> list: ...
def get_bundle(bundle_name: str = None) -> dict: ...
def get_production_bundle() -> dict: ...
def get_staging_bundle() -> dict: ...
def create_bundle(
        name: str,
        addons: dict,
        production=False,
        stage: BundleMode = False,
        installer_version=None,
        dependency_packages=None) -> dict: ...

