import subprocess


class GitChecker():

    def __init__(self, repository_name, directory):
        self.repository_name = repository_name
        self.directory = directory
        self._checkout_branch()
        self._set_merged_list()

    def _checkout_branch(self):
        try:
            subprocess.run(["git", "checkout", f"{self.repository_name}"], cwd=self.directory)
        except Exception:
            raise ValueError(f'{self.repository_name}をチェックアウトできません')

        try:
            subprocess.run(f"git pull", shell=True, cwd=self.directory)
        except Exception:
            raise ValueError(f'{self.repository_name}のプルに失敗しました。')

    def _set_merged_list(self):
        self.merged_list = subprocess.run(f"git log --merges --oneline", shell=True,
                cwd=self.directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def merge_check(self, id):
        result = subprocess.run(["grep", f"{id}"], input=self.merged_list.stdout,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.stdout is not None:
            return [id, p2.stdout]
        else:
            return [id, '']
