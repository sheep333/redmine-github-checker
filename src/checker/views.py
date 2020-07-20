import pandas as pd

from django.http import HttpResponse
from django.shortcuts import render

from .forms import (GitBranchForm, RedmineAuthForm, RedmineIssueFilterForm,
                    RedmineIssueFilterFormset, RedmineIssueEmptyFilterFormset)
from .redmine import RedmineModule
from .git_checker import GitChecker


def home(request):
    auth_form = RedmineAuthForm(request.POST or None)
    issue_filter_form = RedmineIssueFilterFormset(request.POST or None, prefix='issue_filter')
    issue_empty_filter_form = RedmineIssueEmptyFilterFormset(request.POST or None, prefix='issue_empty_filter')
    git_branch_form = GitBranchForm(request.POST or None)

    context = {
        'auth_form': auth_form,
        'issue_filter_form': issue_filter_form,
        'issue_empty_filter_form': issue_empty_filter_form,
        'git_branch_form': git_branch_form,
    }

    if request.method == "POST" and \
            auth_form.is_valid() and issue_filter_form.is_valid() and \
            issue_empty_filter_form.is_valid() and git_branch_form.is_valid():

        # RedmineのIssueフィルターをマージしてIssueを検索
        redmine = RedmineModule(**auth_form.cleaned_data)
        params = {}
        for data in issue_filter_form.cleaned_data:
            if data:
                params.update(data)
        for data in issue_empty_filter_form.cleaned_data:
            if data:
                params.update(data)

        issues = redmine.filter_issues(**params)

        # Githubのマージされたブランチと比較
        result = []
        branch_name = git_branch_form.cleaned_data.get('branch_name')
        directory = git_branch_form.cleaned_data.get('directory')
        git_checker = GitChecker(branch_name, directory)
        for issue in issues:
            result += git_checker.merge_check(issue.id)

        # CSV化する
        df = pd.DataFrame(result, columns=['issue_id', 'output'])
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=filename.csv'
        df.to_csv(path_or_buf=response, index=False)

        return response

    return render(request, 'checker/index.html', context)
