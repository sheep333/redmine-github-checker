import subprocess


class GitChecker():

    def __init__(self, repository_name, directory):
        self.repository_name = repository_name
        self.directory = directory
        self._checkout_branch()

    def _checkout_branch(self):
        try:
            subprocess.run(["git", "checkout", f"{self.repository_name}"], cwd=self.directory)
        except Exception:
            raise ValueError(f'{self.repository_name}をチェックアウトできません')

        try:
            subprocess.run(f"git pull", shell=True, cwd=self.directory)
        except Exception:
            raise ValueError(f'{self.repository_name}のプルに失敗しました。')

    def merge_check(self, id):
        p1 = subprocess.Popen(["git", "log", "--merges", "--oneline"], cwd=self.directory,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p2 = subprocess.Popen(["grep", f"{id}"], stdin=p1.stdout, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True)
        p1.stdout.close()
        output = p2.communicate()[0]

        if output is not None:
            return [id, output]
        else:
            return [id, '']

        p2.returncode # grep の終了コード
