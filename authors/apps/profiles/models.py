import hashlib

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save

from authors.apps.core.models import TimeStampModel
from authors import settings


class Profile(TimeStampModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)
    birth_date = models.DateField(_('last name'), null=True, blank=True)
    bio = models.TextField(_('bio'), default='', null=True, blank=True)
    avatar = models.URLField(_('avatar'), null=True, blank=True)
    city = models.CharField(_('city'), blank=True, null=True, max_length=100, default='')
    country = models.CharField(_('country'), blank=True, null=True, max_length=100, default='')
    phone = models.IntegerField(_('phone'), blank=True, null=True, default=0)
    website = models.URLField(_('website'), blank=True, null=True, default='')
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
    username = models.CharField(_('username'), max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def follow(self, profile):
        self.follows.add(profile)

    def unfollow(self, profile):
        self.follows.remove(profile)

    def followers(self, profile):
        return profile.followed_by.all()

    def following(self, profile):
        return profile.follows.all()


"""
Generate gravatar url from a user's email
"""


def gravatar_url(email):
    # Get the md5 hash of the email address
    md5 = hashlib.md5(email.encode())
    digest = md5.hexdigest()
    return 'http://www.gravatar.com/avatar/{}'.format(digest)


"""
Signal receiver for 'post_save' signal sent by User model upon saving
"""


def create_profile(sender, **kwargs):
    if kwargs.get('created'):
        user_profile = Profile(user=kwargs.get('instance'))
        user_profile.avatar = gravatar_url(user_profile.user.email)
        user_profile.username = kwargs.get('instance').username
        user_profile.save()


# connect the signal to the handler function
post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL)
