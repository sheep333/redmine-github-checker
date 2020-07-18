from redminelib import Redmine


class RedmineModule():
    params = ["project_id", "subject", "tracker_id", "description", "status_id", "priority_id",
              "category_id", "fixed_version_id", "is_private", "assigned_to_id", "watcher_user_ids",
              "parent_issue_id", "start_date", "due_date", "estimated_hours", "done_ratio", "custom_fields", "uploads"]

    def __init__(self, **kwargs):
        # urlとkeyは必須
        self.redmine = Redmine(**kwargs)

    def get_project(self, project_id):
        return self.redmine.project.get(project_id)

    def get_issues(self, project_id):
        return self.redmine.issue.filter(project_id=project_id)

    def filter_issues(self, **kwargs):
        return self.redmine.issue.filter(**kwargs)
