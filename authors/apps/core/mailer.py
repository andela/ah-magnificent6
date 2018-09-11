# Custom mail sender

from django.core.mail import send_mail


class SendMail:

    def __init__(self, subject, message, email_from, to):
        self.subject = subject
        self.message = message
        self.receipt = email_from
        self.to = to

    def send(self):
        send_mail(self.subject, self.message, self.receipt, [self.to])
