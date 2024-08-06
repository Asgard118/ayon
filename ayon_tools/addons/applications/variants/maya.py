from .base import AppVariant


class MayaVariant(AppVariant):
    app_name = "maya"
    default_windows_path = r"C:\Program Files\Autodesk\Maya{version}\bin\maya.exe"
    default_linux_path = "/usr/autodesk/maya{version}/bin/maya"
    default_darwin_path = "/Applications/Autodesk/maya{version}/Maya.app"

    def get_default_environment(self):
        return {"MAYA_VERSION": "{version}"}
