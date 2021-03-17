from django import forms


class GetFile(forms.Form):
    token = forms.CharField(max_length=256)
    file_id = forms.CharField(max_length=256)


class UploadFile(forms.Form):
    token = forms.CharField(max_length=256)
    file_name = forms.CharField(max_length=512)
    file = forms.FileField()
