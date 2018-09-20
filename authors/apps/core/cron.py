from django_cron import CronJobBase, Schedule

from authors.apps.authentication.models import User
from authors.apps.profiles.models import Profile
from authors.apps.articles.models import Article
# from authors.apps.notifications.models import Notification
from django.utils.timesince import timesince


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 120 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'authors.apps.core.cron.MyCronJob'  # a unique code

    def send_notifications(self):
        print('dfgg')
        # notifications = Notification.objects.all()
        # for notification in notifications:
        #     if timesince(notification.created_at, None) < RUN_EVERY_MINS:
        #         notified = notification.notified.all()
        #         for user in notified:
        #             send



# from celery import task
# from celery.decorators import periodic_task
# from celery.task.schedules import crontab
# from celery.utils.log import get_task_logger


# @periodic_task(run_every=crontab(minute="0", hour="23"))
# def do_every_midnight():
#     print("rtyuikjmhgfds")