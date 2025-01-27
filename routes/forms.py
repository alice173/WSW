from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from .models import Route

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['title', 'date', 'start_point', 'end_point', 'route_img', 
                 'time_taken', 'comments', 'distance', 'elevation']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Add a name for your walk'
            }),
            'start_point': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Search for start point or use the map', 
                'list': 'start-suggestions',
                'autocomplete': 'off'
            }),
            'end_point': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Search for end point or use the map', 
                'list': 'end-suggestions',
                'autocomplete': 'off'
            }),
            'time_taken': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Add time in hours'
            }),
            'route_img': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'comments': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter comments'
            }),
            'distance': forms.HiddenInput(),  
            'elevation': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
                'comments',
                'distance',  
                'elevation'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn')
            )
        )

    def clean(self):
        """
        Custom clean method to handle any special validation
        """
        cleaned_data = super().clean()
        # Add any custom validation here if needed
        return cleaned_data

    def save(self, commit=True):
        """
        Override save method to handle any special processing
        """
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance