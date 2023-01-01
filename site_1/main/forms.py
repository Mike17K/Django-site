from django import forms


class CreateNewTable(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    
class CreateNewCanvas(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    image = forms.ImageField(label="Image")
    show = forms.BooleanField(required=False)
    