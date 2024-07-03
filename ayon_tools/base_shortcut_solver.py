class Solver:
    """
    У каждого солвера своя задача. Он знает какие файлы нужн осчитать
    и как из собрать в один словарь
    """

    name = None

    def solve(self, project: str = None):
        raise NotImplementedError
