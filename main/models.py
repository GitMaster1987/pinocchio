from django.db import models


# Create your models here.
class Menu(models.Model):
    title = models.CharField(
        max_length=20, blank=False, null=False, verbose_name="Название раздела"
    )
    slug = models.SlugField(max_length=20, blank=False, null=False, verbose_name="URL")

    class Meta:
        db_table = "menu"
        verbose_name = "Меню"
        verbose_name_plural = "Меню"

    def __str__(self):
        return str(self.pk) + " - " + self.title
