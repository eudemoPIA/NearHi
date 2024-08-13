from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'time', 'location', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'maxlength': 800, 'rows': 5}),
        }
