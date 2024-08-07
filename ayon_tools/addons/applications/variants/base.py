import json


class _SafeDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"


class AppVariant:
    app_name = None
    app_label = None
    default_windows_path = None
    default_linux_path = None
    default_darwin_path = None

    def __init__(self, shortcut_data: dict):
        if isinstance(shortcut_data, (int, str)):
            shortcut_data = {"name": str(shortcut_data)}
        self.shortcut_data = shortcut_data
        self.variant_name = shortcut_data["name"]
        self.variant_label = (
            shortcut_data.get("label") or self.app_label or self.variant_name.title()
        )

    @staticmethod
    def _safe_format(value, **kwargs):
        return value.format_map(_SafeDict(kwargs))

    def _format_variables(self, string):
        return self._safe_format(string, **self.get_format_variables())

    def get_format_variables(self):
        return dict(
            label=self.variant_label,
            version=self.variant_name,
            name=self.variant_name,
        )

    def get_default_executable_paths(self):
        windows_path = (
            self._format_variables(self.default_windows_path)
            if self.default_windows_path
            else None
        )
        linux_path = (
            self._format_variables(self.default_linux_path)
            if self.default_linux_path
            else None
        )
        darwin_path = (
            self._format_variables(self.default_darwin_path)
            if self.default_darwin_path
            else None
        )
        return {
            "windows": windows_path,
            "linux": linux_path,
            "darwin": darwin_path,
        }

    def get_custom_executables(self):
        if "executables" in self.shortcut_data:
            return self.shortcut_data["executables"]
        return {}

    def get_executable_paths(self):
        # default paths
        exec_paths = self.get_default_executable_paths()
        # custom paths from shortcuts
        for os_name, paths in self.get_custom_executables().items():
            if os_name in exec_paths and exec_paths[os_name]:
                exec_paths[os_name].extend(paths)
            else:
                exec_paths[os_name] = paths
        # filter None values and duplicates
        for os_name, paths in exec_paths.items():
            exec_paths[os_name] = list(set([p for p in paths if p]))
        return exec_paths

    def get_default_environment(self):
        return {}

    def get_environment(self):
        env = self.get_default_environment()
        if "environment" in self.shortcut_data.keys():
            for k, v in self.shortcut_data["environment"].items():
                if isinstance(v, str):
                    v = self._format_variables(v)
                env[k] = v
        return env

    def get_default_arguments(self):
        return {"windows": [], "linux": [], "darwin": []}

    def get_arguments(self):
        """
        1.
        arguments:
            - "--arg value"
        2.
        arguments:
            windows:
                - "--arg value"
            linux:
                - "--arg value"
        """
        arguments = self.get_default_arguments()
        args = self.shortcut_data.get("arguments")
        if args is None:
            return arguments
        elif isinstance(args, list):
            for os_name in arguments.keys():
                arguments[os_name].extend(args)
        elif isinstance(args, dict):
            for os_name, arg_list in args.items():
                if not isinstance(arg_list, list):
                    raise TypeError("Arguments must be a list")
                arguments[os_name].extend(arg_list)
        return arguments

    @property
    def use_python_2(self):
        return False

    def get_config(self):
        windows_path, linux_path, darwin_path = self.get_default_executable_paths()
        env = self.get_environment()
        return {
            "name": self.variant_name,
            "label": self.variant_label,
            "environment": json.dumps(env),
            "use_python_2": self.use_python_2,
            "executables": {
                "windows": [windows_path],
                "linux": [linux_path],
                "darwin": [darwin_path],
            },
            "arguments": self.get_arguments(),
        }
