from .base import AppVariant

class HoudiniVariant(AppVariant):
	app_name = 'houdini'
	default_windows_path = "C:\\Program Files\\Side Effects Software\\Houdini {label}\\bin\\houdini.exe"
	linux_path = "/opt/hfs{label}/bin/houdinifx"
	darwin_path = []

	def _format_variables(self, string):
		return string.format(
			label=self.variant_label,
			version=self.variant_name,
			name=self.variant_name,
		)