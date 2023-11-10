from django import forms


class UploadRequirementsForm(forms.Form):
    name = forms.CharField(
        label='Name',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    information_required = forms.FileField(
        label='Upload Required Information',
        required=False
    )
    comment = forms.CharField(
        label='Auditee Comment',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

