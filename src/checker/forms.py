from os import getenv
from django import forms
from django.core.exceptions import ValidationError


class RedmineAuthForm(forms.Form):
    url = forms.URLField(required=True)
    user = forms.CharField(max_length=255, required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    def clean(self):
        super().clean()
        data = self.cleaned_data

        if 'user' not in data or 'password' not in data:
            key = getenv('REDMINE_KEY')
            if key:
                data['key'] = key
            else:
                raise ValidationError('Redmineの認証に必要な値が存在しません。')
        return data


class RedmineIssueFilterForm(forms.Form):
    CHOICES = [
        ('project_id', 'プロジェクトID'),
        ('fixed_version_id', 'バージョンID'),
        ('tracker_id', 'トラッカーID'),
        ('status_id', 'ステータスID'),
        ('due_date', '期限日'),
    ]
    param = forms.ChoiceField(choices=CHOICES, required=False)
    value = forms.CharField(max_length=255, required=False)


class RedmineIssueEmptyFilterForm(forms.Form):
    param = forms.CharField(max_length=50, required=False)
    value = forms.CharField(max_length=255, required=False)


class GitBranchForm(forms.Form):
    branch_name = forms.CharField(max_length=255, required=False)


RedmineIssueFilterFormset = forms.formset_factory(RedmineIssueFilterForm, extra=5)
RedmineIssueEmptyFilterFormset = forms.formset_factory(RedmineIssueEmptyFilterForm, extra=5)
