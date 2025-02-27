from django.db import models
from django.utils import timezone


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
    

# Model Banner
class Banner(models.Model):
    title = models.CharField(
        max_length=100, blank=False, null=False, verbose_name="Заголовок"
    )
    image = models.ImageField(upload_to='banner_img', blank=False, null=False,  verbose_name='Картинка')
    price = models.FloatField(default=0.0, blank=False, null=False, verbose_name='Цена')
    width = models.IntegerField(default=450, verbose_name='Ширина')
    height = models.IntegerField(default=350, verbose_name='Высота')
    created_at = models.DateTimeField( verbose_name="Дата записи", default=timezone.now)
    update_at = models.DateTimeField( verbose_name="Дата обновления", blank=False, null=False)

    class Meta:
        db_table = "banners"
        verbose_name = "Баннер"
        verbose_name_plural = "Баннер"
    
    def __str__(self):
        return str(self.pk) + " - " + self.title
