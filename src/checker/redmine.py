from redminelib import Redmine


class RedmineModule():

    def __init__(self, **kwargs):
        # urlとkeyは必須
        self.redmine = Redmine(**kwargs)

    def get_project(self, project_id):
        return self.project.get(project_id)

    def get_issues(self, project_id):
        return self.issue.filter(project_id=project_id)

    def filter_issues(self, **kwargs):
        return self.issue.filter(**kwargs)
