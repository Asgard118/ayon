from ayon_tools.studio import StudioSettings


def process(studio_name: str | None):
    studio = StudioSettings(studio_name)
    print(f"Studio: {studio.name}")
