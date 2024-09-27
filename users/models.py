from django.db import models
from django.contrib.auth.models import User
from secrets import token_hex

# Create your models here.


class Token(models.Model):
    user = models.OneToOneField(
        to=User,
        verbose_name="user",
        on_delete=models.CASCADE
    )
    key = models.CharField(
        verbose_name="key",
        unique=True,
        max_length=40
    )
    created_at = models.DateTimeField(
        verbose_name="create at",
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = token_hex(20)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.key
