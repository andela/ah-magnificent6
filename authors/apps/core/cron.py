from django_cron import CronJobBase, Schedule
from django.utils.timesince import timesince
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from authors.apps.notifications.models import Notification


class EmailNotificationCron(CronJobBase):
    """Create the cron job for email sending."""

    RUN_EVERY_MINS = settings.RUN_EVERY_MINS
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'authors.apps.core.cron.MyCronJob'  # a unique code

    def do(self):
        """Send emails to all the persons to be notified."""
        subject = 'Authors Haven Notification'

        recipients = []
        notifications = Notification.objects.all()
        for notification in notifications:
            if notification.email_sent == False:
                for user in notification.notified.all():
                    if user not in notification.read.all():
                        if user.profile.email_notification_enabled == True:
                            recipients.append(user.email)
                content = {'notification': notification}
                message = render_to_string("notification.html", content)
                mail = EmailMessage(
                    subject=subject,
                    body=message,
                    to=recipients,
                    from_email=settings.EMAIL_HOST_USER)
                mail.content_subtype = "html"
                mail.send(fail_silently=False)
                notification.email_sent = True
                notification.save()
