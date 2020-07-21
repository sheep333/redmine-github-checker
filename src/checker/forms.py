from os import getenv

from django import forms
from django.core.exceptions import ValidationError

from .redmine import RedmineModule


class RedmineAuthForm(forms.Form):
    url = forms.URLField(
        required=True,
        help_text='RedmineのURLを入力してください(必須)。',
    )
    username = forms.CharField(
        max_length=255,
        required=False,
        help_text='Redmineのユーザ名を入力してください(入力しない場合にはAPI KEYを環境変数に指定してください)。',
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        help_text='Redmineのパスワードを入力してください(入力しない場合にはAPI KEYを環境変数に指定してください)。',
    )

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
    param = forms.CharField(
        max_length=50,
        help_text='RedmineでIssueのフィルターに使用できるパラメータを入力してください'
    )
    value = forms.CharField(
        max_length=255,
        help_text='RedmineでIssueのフィルターに設定する値を入力してください'
    )

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

    param = forms.ChoiceField(
        choices=CHOICES,
        required=False,
        initial='none',
        help_text='RedmineのIssueのフィルターを選択してください'
    )


class GitBranchForm(forms.Form):
    branch_name = forms.CharField(
        max_length=255,
        required=False,
        help_text='マージ状況を確認したいブランチ名を入力してください'
    )
    directory = forms.CharField(
        max_length=512,
        required=False,
        help_text='確認するGitのリポジトリを入力してください'
    )

    def clean_branch_name(self):
        data = self.cleaned_data['branch_name']
        # 値が入っていなかったら環境変数からブランチ名を取得
        if not data:
            data = getenv('BRANCH_NAME')
            if not data:
                raise ValidationError('ブランチ名が存在しません。')
        return data

    def clean_directory(self):
        data = self.cleaned_data['directory']
        # 値が入っていなかったら環境変数からディレクトリ名を取得
        if not data:
            data = getenv('DIRECTORY')
            if not data:
                raise ValidationError('ディレクトリ名が存在しません。')
        return data


class RedmineFilterFormSet(forms.BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        # パラメータの重複チェック
        params = []
        for form in self.forms:
            data = form.cleaned_data
            if data.get('param') and (data['param'] in params):
                raise forms.ValidationError("同じパラメータが含まれる場合には|区切りで入力してください。")
            else:
                params += data


# RedmineIssueFilterForm.CHOICESの中から1つ以上のパラメータ入力を必須とする
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
