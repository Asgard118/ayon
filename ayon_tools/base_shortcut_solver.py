from ayon_tools.studio import StudioSettings


class Solver:
    """
    У каждого солвера своя задача. Он знает какие файлы нужн осчитать
    и как из собрать в один словарь
    """

    name = None

    def __init__(self, studio: StudioSettings):
        self.studio = studio

    def solve(self, project: str = None):
        raise NotImplementedError
