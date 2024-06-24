from ayon_tools.studio import Studio


def show_studio_info(studio_name: str | None):
    studio = Studio(studio_name)
    print(f"Studio: {studio.name}")

