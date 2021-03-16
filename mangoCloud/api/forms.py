from django import forms


class GetFile(forms.Form):
    token = forms.CharField(max_length=512)
    file_id = forms.CharField(max_length=512)
