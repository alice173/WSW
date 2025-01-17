from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from .models import Route

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['title', 'date', 'start_point', 'end_point',  'route_img', 'time_taken', 'comments', 'distance', 'elevation']
        widgets = { 'date': forms.DateInput(attrs={'type': 'date'}),
        'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add a name for your walk'}),
        'start_point': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter start point or use the map'}),
        'end_point': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter end point or use the map'}),
        'time_taken': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Add time in hours'}),
        'route_img': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        'comments': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter comments'}),
        'distance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter distance in miles'}),
        'elevation': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter elevation gain in meters'}),
        }

    def __init__(self, *args, **kwargs):
        super(RouteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Your Form Title',
                'title',
                'date',
                'start_point',
                'end_point',
                'route_img',
                'time_taken',
                'comments'
                 'distance',  # Hidden field
                'elevation'  # Hidden field
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-primary')
            )
        )