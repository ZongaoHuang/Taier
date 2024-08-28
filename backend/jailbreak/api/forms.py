# csv_app/forms.py

from django import forms


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()

class JsonUploadForm(forms.Form):
    file = forms.FileField()
    set_id = forms.IntegerField()
