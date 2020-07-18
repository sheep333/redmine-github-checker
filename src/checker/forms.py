from os import getenv

from django import forms
from django.core.exceptions import ValidationError

from .redmine import RedmineModule


class RedmineAuthForm(forms.Form):
    url = forms.URLField(required=True)
    username = forms.CharField(max_length=255, required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    def clean(self):
        data = super().clean()
        # ユーザとパスワードがなかったら環境変数からAPI KEYを取得
        if 'username' not in data or 'password' not in data:
            key = getenv('REDMINE_KEY')
            if key:
                data['key'] = key
            else:
                raise ValidationError('Redmineの認証に必要な値が存在しません。')
        return data


class RedmineIssueEmptyFilterForm(forms.Form):
    param = forms.CharField(max_length=50, required=False)
    value = forms.CharField(max_length=255, required=False)

    def clean(self):
        data = super().clean()
        if data.get('param'):
            return_data = { data['param']: data['value'] }
            return return_data

    def clean_param(self):
        param = self.cleaned_data["param"]

        params = RedmineModule.params
        if param not in params:
            self.add_error('param', f'{param}は使用できないパラメータです。')
        else:
            return param


class RedmineIssueFilterForm(RedmineIssueEmptyFilterForm):
    CHOICES = [
        ('none', '-------'),
        ('project_id', 'プロジェクトID'),
        ('fixed_version_id', 'バージョンID'),
        ('tracker_id', 'トラッカーID'),
        ('status_id', 'ステータスID'),
        ('due_date', '期限日'),
    ]

    param = forms.ChoiceField(choices=CHOICES, required=False, initial='none')


class GitBranchForm(forms.Form):
    branch_name = forms.CharField(max_length=255)


class RedmineFilterFormSet(forms.BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        for form in self.forms:
            data = form.cleaned_data
            if data.get('param') and (data['param'] in params):
                raise forms.ValidationError("同じパラメータが含まれる場合には|区切りで入力してください。")


RedmineIssueFilterFormset = forms.formset_factory(
    RedmineIssueFilterForm,
    formset=RedmineFilterFormSet,
    extra=3,
    min_num=1,
    validate_min=True,
)

RedmineIssueEmptyFilterFormset = forms.formset_factory(
    RedmineIssueEmptyFilterForm,
    formset=RedmineFilterFormSet,
    extra=3,
)
