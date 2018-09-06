from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save

from authors import settings


GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(default='', null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars', blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    city = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=100, default='')
    phone_number = models.IntegerField(default=0)
    website = models.URLField(default='', blank=True)
    following = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs.get('created'):
        user_profile = UserProfile.objects.create(user=kwargs.get('instance')

post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL)
