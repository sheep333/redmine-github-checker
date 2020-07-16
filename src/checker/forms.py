from django import forms


class RedmineForm(forms.Form):
    url = forms.URLField(required=True)
    user = forms.CharField(max_length=255, required=False)
    password = forms.CharField(widget=forms.Passwordnput, required=False)


class CheckProjectForm(forms.Form):
    project = forms.CharField(max_length=255, required=False)


class CheckVersionForm(forms.Form):
    version = forms.CharField(max_length=255, required=False)


class CheckGithubBranchForm(forms.Form):
    github_branch = forms.CharField(max_length=255, required=False)
