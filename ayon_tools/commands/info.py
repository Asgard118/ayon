from ayon_tools.studio import StudioSettings


def run(studio_name: str or None, **kwargs):
    studio = StudioSettings(studio_name)
    print(f"Studio: {studio.name}")
