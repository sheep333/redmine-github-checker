import subprocess


class GitChecker():

    def __init__(self, repository_name, directory):
        self.repository_name = repository_name
        self.directory = directory
        self._checkout_branch()

    def _checkout_branch(self):
        try:
            subprocess.run(f"git checkout {self.repository_name}", shell=True, cwd=self.directory)
        except Exception:
            raise ValueError(f'{self.repository_name}をチェックアウトできません')

        try:
            subprocess.run(f"git pull", shell=True, cwd=self.directory)
        except Exception:
            raise ValueError(f'{self.repository_name}のプルに失敗しました。')

    def merge_check(self, id):
        command = f"git log --merges --oneline|grep {id}"
        output = subprocess.run(command, shell=True, cwd=self.directory)
        if output is not None:
            return [id, output]
        else:
            return [id, '']
