class AyonToolError(Exception):
    pass


class ConfigError(AyonToolError):
    pass


class RepositoryDataError(AyonToolError):
    pass


class ServerDataError(AyonToolError):
    pass


class GitError(AyonToolError):
    pass


class AnatomyUpdateError(AyonToolError):
    pass


class AnatomyConflictError(AnatomyUpdateError):
    pass


class DepPackageNotExists(AyonToolError):
    pass


class DepPackageAlreadyInstalled(AyonToolError):
    pass
