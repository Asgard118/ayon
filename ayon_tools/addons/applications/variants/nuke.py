from .base import AppVariant


class NukeVariant(AppVariant):
    app_name = "nuke"
    default_windows_path = "C:\\Program Files\\Nuke{label}\\Nuke{version}.exe"
    linux_path = "/usr/local/Nuke{label}/Nuke{version}"
    darwin_path = "/Applications/Nuke{label}/Nuke{label}.app"

    def _format_variables(self, string):
        return string.format(
            label=self.variant_label,
            version=self.variant_name.split("v")[0],
            name=self.variant_name,
        )


class NukeXVariant(NukeVariant):
    app_name = "nukex"
    app_label = "NukeX"
    default_darwin_path = "/Applications/Nuke{label}/NukeX{label}.app"

    def get_default_arguments(self):
        return {
            "windows": ["--nukex"],
            "linux": ["--nukex"],
            "darwin": [],
        }


class NukeStudioVariant(NukeVariant):
    app_name = "nukestudio"
    app_label = "NukeStudio"
    default_darwin_path = "/Applications/Nuke{label}/NukeStudio{label}.app"

    def get_default_arguments(self):
        return {
            "windows": ["--studio"],
            "linux": ["--studio"],
            "darwin": [],
        }


class NukeAssistVariant(NukeVariant):
    app_name = "nukeassist"
    app_label = "NukeAssist"
    default_darwin_path = "/Applications/Nuke{label}/NukeAssist{label}.app"

    def get_default_arguments(self):
        return {
            "windows": ["--nukeassist"],
            "linux": ["--nukeassist"],
            "darwin": [],
        }


class HieroVariant(NukeVariant):
    app_name = "hiero"
    default_darwin_path = "/Applications/Nuke{label}/Hiero{label}.app"

    def get_default_arguments(self):
        return {
            "windows": ["--hiero"],
            "linux": ["--hiero"],
            "darwin": [],
        }
