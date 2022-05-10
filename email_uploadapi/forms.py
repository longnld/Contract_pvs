from django import forms
from.models import Email_email
class EmailFormUpdate(forms.Form):
    status=forms.CharField( max_length=255, required=False)
    Subject=forms.CharField(max_length=255,required=False)
    note=forms.CharField(max_length=255,required=False)
    class Meta:
        fields=['status','Subject','note']