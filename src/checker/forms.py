from django import forms


class RedmineAuthForm(forms.Form):
    url = forms.URLField(required=True)
    user = forms.CharField(max_length=255, required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)


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


class GitBranchForm(forms.Form):
    branch_name = forms.CharField(max_length=255, required=False)
