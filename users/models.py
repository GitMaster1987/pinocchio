from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(
        max_length=20,  # Adjust based on your needs
        validators=[
            RegexValidator(
                regex=r"^\+7\s\(\d{3}\)\s\d{3}-\d{2}-\d{2}$",  # Example regex for international phone numbers
                message="Номер телефона должен быть в формате: '+7 (***) ***-**-**'.",
            )
        ],
        verbose_name="Номер телефона",
        blank=False,
        null=False,
    )

    class Meta:
        db_table = "user"
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return str(self.pk) +" - " + self.username

    