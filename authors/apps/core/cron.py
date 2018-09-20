from django_cron import CronJobBase, Schedule

from authors.apps.notifications.models import Notification
from django.utils.timesince import timesince
from django.core.mail import send_mail
from django.conf import settings


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'authors.apps.core.cron.MyCronJob'  # a unique code

    def do(self):
        """send emails to all the persons to be notified"""
        subject = 'Authors Haven Notification'

        emails = []
        notifications = Notification.objects.all()
        for notification in notifications:
            if notification.email_sent == False:
                for user in notification.notified.all():
                    if user.profile.email_notification_enabled == True:
                        emails.append(user.email)
                        send_mail(
                            subject,
                            notification.notification,
                            settings.EMAIL_HOST_USER,
                            emails,
                            fail_silently=False)
                        notification.email_sent = True
                        notification.save()
