import pandas as pd

from django.http import HttpResponse
from django.shortcuts import render

from .forms import GitBranchForm, RedmineAuthForm, RedmineIssueFilterForm
from .redmine import Redmine
from .git_checker import GitChecker


def home(request):
    auth_form = RedmineAuthForm(request.POST or None)
    issue_filter_form = RedmineIssueFilterForm(request.POST or None)
    git_branch_form = GitBranchForm(request.POST or None)

    context = {
        'auth_form': auth_form,
        'issue_filter_form': issue_filter_form,
        'git_branch_form': git_branch_form,
    }

    if request.method == "POST" and auth_form.is_valid() and \
            issue_filter_form.is_valid() and git_branch_form.is_valid():

        redmine = Redmine(**auth_form.cleaned_data)
        issues = redmine.filter_issues(**issue_filter_form.cleaned_data)

        result = []
        git_checker = GitChecker(**git_branch_form.cleaned_data)
        for issue in issues:
            result += git_checker(issue.issue_id)

        df = pd.DataFrame(result, columns=['issue_id', 'output'])
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=filename.csv'
        df.to_csv(path_or_buf=response, index=False)

        return response

    return render(request, 'checker/index.html', context)
