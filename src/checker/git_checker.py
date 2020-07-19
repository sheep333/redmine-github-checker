import subprocess


class GitChecker():

    def __init__(self, repository_name, directory):
        self.repository_name = repository_name
        self.directory = directory
        self._checkout_branch()

    def _checkout_branch(self):
        try:
            subprocess.call(f"cd {self.directory}", shell=True)
        except Exception:
            raise ValueError(f'{self.directory}に移動できません。')

        try:
            subprocess.call(f"git checkout {self.repository_name}", shell=True)
        except Exception:
            raise ValueError(f'{self.repository_name}をチェックアウトできません')

        try:
            subprocess.call(f"git pull", shell=True)
        except Exception:
            raise ValueError(f'{self.repository_name}のプルに失敗しました。')

    def merge_check(id):
        command = f"git log --merges --oneline|grep {id}"
        output = subprocess.check_output(command, shell=True)
        if output is not None:
            return [id, output]
        else:
            return [id, '']
