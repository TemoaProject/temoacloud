from __future__ import unicode_literals
from django.contrib.auth import get_user_model
# from django.db import models
from datetime import datetime
from uuid import uuid4
from django.conf import settings

from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import ForeignKey, Model, CASCADE
from django.db.models import BooleanField, DateTimeField, TextField, CharField, FileField, UUIDField

from accounts.models import Account, MyAccountManager

MODE_DEFAULT_CHOICE = 'INPUT'
MODE_CHOICES = (
        ('INPUT', 'Input'),
        ('OUTPUT', 'Output'),
        ('Model', 'Model'),
)


# /uploads/projects/project_uid/scenarios/filename
def io_upload_file_to(instance, filename):
    return settings.UPLOADED_PROJECTS_DIR + '{0}/scenarios/{1}'.format(instance.project.uid, filename)


# /uploads/projects/project_uid/files/filename
def upload_file_to(instance, filename):
    return settings.UPLOADED_PROJECTS_DIR + '{0}/files/{1}'.format(instance.project.uid, filename)


class Project(Model):

    uid = UUIDField(default=uuid4)
    name = CharField(max_length=500)
    desc = TextField(null=True)

    account = ForeignKey(Account, on_delete=CASCADE)

    created = DateTimeField(default=now)
    updated = DateTimeField(default=now)


class Scenario(Model):
    uid = UUIDField(default=uuid4)
    name = CharField(max_length=500)

    project = ForeignKey(Project, on_delete=CASCADE)
    account = ForeignKey(Account, on_delete=CASCADE)


    created = DateTimeField(default=now)
    updated = DateTimeField(default=now)


class DataFile(Model):

    uid = UUIDField(default=uuid4)
    file = FileField(upload_to=upload_file_to, max_length=500)
    name = CharField(max_length=500, default='')

    project = ForeignKey(Project, on_delete=CASCADE)
    account = ForeignKey(Account, on_delete=CASCADE)
    scenario = ForeignKey(Scenario, on_delete=CASCADE)

    created = DateTimeField(default=now)
    updated = DateTimeField(default=now)


class Actions(Model):
    uid = UUIDField(default=uuid4)
    name = CharField(max_length=500)
    mode = CharField(max_length=10, choices=MODE_CHOICES, default=MODE_DEFAULT_CHOICE)
    desc = TextField(null=True)

    project = ForeignKey(Project, on_delete=CASCADE)
    account = ForeignKey(Account, on_delete=CASCADE)
    scenario = ForeignKey(Scenario, on_delete=CASCADE)

    created = DateTimeField(default=now)
    updated = DateTimeField(default=now)


class CommTech(Model):
    name = CharField(max_length=50)
    value = CharField(max_length=50)

    project = ForeignKey(Project, on_delete=CASCADE)
    account = ForeignKey(Account, on_delete=CASCADE)
    actions = ForeignKey(Actions, on_delete=CASCADE)
    scenario = ForeignKey(Scenario, on_delete=CASCADE)

    created = DateTimeField(default=now)
    updated = DateTimeField(default=now)

    def comm_tech_method(self):
        if self.name == 'None':
            return self.value == ''


class InputOutputDataFile(Model):

    uid = UUIDField(default=uuid4)
    file = FileField(upload_to=io_upload_file_to, max_length=500)
    mode = CharField(max_length=10, choices=MODE_CHOICES, default=MODE_DEFAULT_CHOICE)
    name = CharField(max_length=500, default='')

    project = ForeignKey(Project, on_delete=CASCADE)
    account = ForeignKey(Account, on_delete=CASCADE)
    actions = ForeignKey(Actions, on_delete=CASCADE)
    scenario = ForeignKey(Scenario, on_delete=CASCADE)

    created = DateTimeField(default=now)
    updated = DateTimeField(default=now)


class InputDataRun(Model):
    uid = UUIDField(default=uuid4)

    color_scheme = CharField(max_length=50)
    output_format = CharField(max_length=50)

    input_file = ForeignKey(InputOutputDataFile, on_delete=CASCADE,  null=True)
    comm_tech = ForeignKey(CommTech, on_delete=CASCADE)

    actions = ForeignKey(Actions, on_delete=CASCADE)
    project = ForeignKey(Project, on_delete=CASCADE)
    account = ForeignKey(Account, on_delete=CASCADE)
    scenario = ForeignKey(Scenario, on_delete=CASCADE)

    # run_datetime = DateTimeField(default=now)  # we may not need it see date_created
    created = DateTimeField(default=now)
    updated = DateTimeField(default=now)


class ModelRun(Model):
    uid = UUIDField(default=uuid4)
    create_spreadsheet = BooleanField(null=True)
    create_text_file_output = BooleanField(null=True)
    generate_lp_file = BooleanField(null=True)
    neos_server = BooleanField(null=True)
    solver = CharField(max_length=50)
    run_option = CharField(max_length=20, null=True)
    mga_slack_value = CharField(max_length=20, null=True)
    mga_iterations = CharField(max_length=20, null=True)
    mga_weighting_method = CharField(max_length=20, null=True)
    scenario_name = CharField(max_length=100, null=True)
    custom_flags = CharField(max_length=200, null=True)

    input = ForeignKey(InputOutputDataFile, on_delete=CASCADE, null=True, related_name="input")
    output = ForeignKey(InputOutputDataFile, on_delete=CASCADE, null=True, related_name="output")

    actions = ForeignKey(Actions, on_delete=CASCADE)
    project = ForeignKey(Project, on_delete=CASCADE)
    account = ForeignKey(Account, on_delete=CASCADE)
    scenario = ForeignKey(Scenario, on_delete=CASCADE)

    # run_datetime = DateTimeField(default=now)
    created = DateTimeField(default=now)
    updated = DateTimeField(default=now)

    def run(self, run_option):
        if run_option == "Single Run":
            self.mga_slack_value = ''
            self.mga_iterations = ''
            self.mga_weighting_method = ''


class OutputDataRun(Model):
    uid = UUIDField(default=uuid4)
    color_scheme = CharField(max_length=20)
    output_format = CharField(max_length=20)

    sectors = CharField(max_length=50, null=True)
    plot_type = CharField(max_length=50, null=True)
    year = CharField(max_length=20,
                     validators=[MinValueValidator(1900), MaxValueValidator(datetime.now().year)],
                     help_text="Use the following format: <YYYY>")

    comm_tech = ForeignKey(CommTech, on_delete=CASCADE, null=True)  # DO we need reference or value ?
    model_run = ForeignKey(ModelRun, on_delete=CASCADE, null=True)
    input_file = ForeignKey(InputOutputDataFile, on_delete=CASCADE, null=True)

    actions = ForeignKey(Actions, on_delete=CASCADE)
    project = ForeignKey(Project, on_delete=CASCADE)
    account = ForeignKey(Account, on_delete=CASCADE)
    scenario = ForeignKey(Scenario, on_delete=CASCADE)

    created = DateTimeField(default=now)
    updated = DateTimeField(default=now)
