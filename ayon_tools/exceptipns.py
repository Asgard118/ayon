class AyonToolError(Exception):
    pass


class RepositoryDataError(AyonToolError):
    pass


class ServerDataError(AyonToolError):
    pass


class GitError(AyonToolError):
    pass
