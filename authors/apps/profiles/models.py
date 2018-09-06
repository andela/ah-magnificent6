from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save

from authors import settings

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(_('bio'),default='', null=True, blank=True)
    gender = models.CharField(_('gender'), max_length=6, choices=GENDER_CHOICES)
    avatar = models.ImageField(_('avatar/'), upload_to='avatars', null=True, blank=True)
    city = models.CharField(_('city'), max_length=100, default='')
    country = models.CharField(_('country'), max_length=100, default='')
    phone = models.IntegerField(_('phone'), default=0)
    website = models.URLField(_('website'), default='', blank=True)
    following = models.BooleanField(_('following'), default=False)
    created_at = models.DateTimeField(_('date joined'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs.get('created'):
        user_profile = Profile(user=kwargs.get('instance'))
        user_profile.save()
        
post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL)
