from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    USER_ROLE = [
        ('admin', 'Admin'),
        ('piso', 'Piso'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    phone = models.IntegerField(default='0000000000')
    role = models.CharField(max_length=10, choices=USER_ROLE, default='piso')

    def __str__(self):
        return f'{self.user.username} Profile'
