from ayon_tools.base_shortcut_solver import Solver
from ayon_tools.repository import repo


class AnatomySolver(Solver):
    def solve(self, project: str = None):
        # TODO
        data = repo.get_file_content("defaults/anatomy.json")
        if project:
            try:
                project_data = repo.get_file_content(f"projects/{project}/anatomy.yml")
                print(project_data)
                data.update(project_data)
            except FileNotFoundError:
                pass
        return data
