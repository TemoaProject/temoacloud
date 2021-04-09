from django import forms
from dapp.models import Project
from django.utils.translation import ugettext_lazy as _

mode_choices = [
    ('InputData', 'Input Data'),
    ('OutputData', 'Output Data'),
    ('ModelRun', 'Model Run'),
    ]


class ProjectForm(forms.ModelForm):

    use_required_attribute = False

    class Meta:
        model = Project
        fields = ('name', 'desc')

        labels = {
            'name': _('Project Name'),
            'desc': _('Project Description'),

        }
        help_texts = {
            # 'sortId': _('1 is will come first , 2 second while displaying in front end'),
        }
        error_messages = {
            'name': {
                'min_length': _("Project Name is too short."),
                'max_length': _("Project Name is too long."),
                'required': "Please enter project name",
            },
            'desc': {
                'min_length': _("Description is too short."),
                'max_length': _("Description is too long."),

            },
        }

    def __init__(self, *args, **kwargs):

        super(ProjectForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Project Name',
            'required': 'false'
        })
        self.fields['desc'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Project Description',
        })
        self.fields['desc'].required = False

