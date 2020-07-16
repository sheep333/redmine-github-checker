import pandas as pd

from django.http import HttpResponse

from .forms import RedmineForm
from .redmine import Redmine
from .git_checker import GitChecker


def home(request):
    form = RedmineForm()
    if request.method == "POST" and form.is_valid():
        param_dict = request.POST
        redmine = Redmine(**param_dict)
        issues = redmine.filter_issues(**param_dict)

        result = []
        git_checker = GitChecker(**param_dict)
        for issue in issues:
            result += git_checker(issue.issue_id)

        df = pd.DataFrame(result, columns=['issue_id', 'output'])
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=filename.csv'
        df.to_csv(path_or_buf=response, index=False)

        return response
