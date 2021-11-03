# from django_cron import CronJobBase, Schedule
from dapp.models import Plan, Account, Project, Scenario
from memberships.models import UserMembership, Subscription
from datetime import date, time, timedelta
from django.core.mail import send_mail


def delete_data():
    users = Subscription.objects.filter(active=False)
    for user in users:
        if users.get_next_billing_date + timedelta(days=30).isoformat() == date.today():
            Project.objects.delete(account=user)
            Scenario.object.delete(account=user)

