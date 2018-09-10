from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save

from authors.apps.core.models import TimeStampModel
from authors import settings

class Profile(TimeStampModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(_('bio'),default='', null=True, blank=True)
    avatar = models.URLField(_('avatar'), null=True, blank=True)
    city = models.CharField(_('city'), max_length=100, blank=True, null=True, default='')
    country = models.CharField(_('country'), max_length=100, blank=True, null=True, default='')
    phone = models.IntegerField(_('phone'), blank=True, null=True, default=0)
    website = models.URLField(_('website'), blank=True, null=True, default='')
    # following = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
    
    def __str__(self):
        return self.user.username

"""
Signal receiver for 'post_save' signal sent by User model upon saving
"""
def create_profile(sender, **kwargs):
    if kwargs.get('created'):
        user_profile = Profile(user=kwargs.get('instance'))
        user_profile.save()

# connect the signal to the handler function   
post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL)
