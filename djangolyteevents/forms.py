from .models import Event
class MyForm(forms.ModelForm):
    class Meta:
        model = Event