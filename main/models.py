from django.db import models


# Create your models here.
class Nav(models.Model):
    title = models.CharField(
        max_length=20, blank=False, null=False, verbose_name="Название раздела"
    )
    slug = models.SlugField(max_length=20, blank=False, null=False, verbose_name="URL")

    class Meta:
        db_table = "navigation"
        verbose_name = "Навигация"
        verbose_name_plural = "Навигация"

    def __str__(self):
        return str(self.pk) + " - " + self.title
