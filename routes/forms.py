from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from .models import Route

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['title', 'date', 'start_point', 'end_point', 'distance', 'time_taken', 'elevation', 'route_img', 'time_taken', 'comments']

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
                'distance',
                'duration',
                'elevation',
                'image',
                'time_taken',
                'comments'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-primary')
            )
        )