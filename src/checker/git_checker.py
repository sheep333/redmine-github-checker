import subprocess


class GitChecker():

    def __init__(self, branch_name, directory):
        self.branch_name = branch_name
        self.directory = directory
        self._checkout_branch()

    def _checkout_branch(self):
        try:
            subprocess.run(["git", "checkout", f"{self.branch_name}"], cwd=self.directory)
        except Exception:
            logger.error(f"Can't checkout branch: {self.branch_name}")
            raise ValueError(f'{self.branch_name}をチェックアウトできません')

        try:
            subprocess.run(f"git pull", shell=True, cwd=self.directory)
        except Exception:
            logger.error(f"Can't pull branch: {self.branch_name}")
            raise ValueError(f'{self.branch_name}のプルに失敗しました。')

    def merge_check(self, id):
        # FIXME: 毎回データを取得するよりもtmpファイルを作ってgrepかける方が負担が少ないかも。
        logger.info(f"Check whether merged issue_id: {id}")
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
