from unicodedata import category
from django.db import models
from django.utils import timezone
import math
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from PIL import Image


def validate_image_dimensions(image):
    max_width = 354  # Максимальная ширина
    max_height = 484  # Максимальная высота
    min_width = 354  # Минимальная ширина
    min_height = 484  # Минимальная высота

    img = Image.open(image)
    width, height = img.size

    if width > max_width or height > max_height:
        raise ValidationError(
            _("Ширина или высота изображения превышает допустимые размеры.")
        )
    if width < min_width or height < min_height:
        raise ValidationError(
            _("Ширина или высота изображения меньше допустимых размеров.")
        )


# Модель навигации на сайте.
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
    image = models.ImageField(
        upload_to="banner_img", blank=False, null=False, verbose_name="Картинка"
    )
    price = models.FloatField(default=0.0, blank=False, null=False, verbose_name="Цена")
    width = models.IntegerField(default=450, verbose_name="Ширина")
    height = models.IntegerField(default=350, verbose_name="Высота")
    created_at = models.DateTimeField(verbose_name="Дата записи", default=timezone.now)
    update_at = models.DateTimeField(
        verbose_name="Дата обновления", blank=False, null=False
    )

    class Meta:
        db_table = "banners"
        verbose_name = "Баннер"
        verbose_name_plural = "Баннер"

    def __str__(self):
        return str(self.pk) + " - " + self.title


# >>> Меню нашего заведения
# ''' Категории меню '''
class Categories(models.Model):
    title = models.CharField(
        max_length=20, blank=False, null=False, verbose_name="Категория меню"
    )
    slug = models.SlugField(max_length=20, blank=False, null=False, verbose_name="Slug")
    icon_class = models.CharField(
        max_length=20, blank=False, null=False, verbose_name="Класс для иконки"
    )

    class Meta:
        db_table = "categories"
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"

    def __str__(self):
        return str(self.pk) + " - " + self.title + " (" + self.slug + ")"


# ''' Блюда для сайта '''
class Products(models.Model):
    name = models.CharField(
        max_length=50, blank=False, null=False, verbose_name="Название"
    )
    description = models.TextField(blank=False, null=False, verbose_name="Описание")
    image = models.ImageField(
        upload_to="product_img", blank=False, null=False, verbose_name="Картинка"
    )
    price = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2, verbose_name="Цена"
    )
    discount = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2, verbose_name="Скидка в %"
    )
    category = models.ForeignKey(
        to=Categories, on_delete=models.PROTECT, verbose_name="Категория"
    )

    class Meta:
        db_table = "products"
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"

    def __str__(self):
        return (
            str(self.pk)
            + " - "
            + self.name
            + " ("
            + str(self.price)
            + ")"
            + " - Категория: "
            + self.category.title
        )

    # Cчитаем цену со скидкой
    def sell_price(self):
        if self.discount:
            return math.ceil(round(self.price - (self.price * self.discount / 100), 2))

        return self.price


# ''' Шеф-повора '''
class Chefs(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False, verbose_name="Имя")
    lastName = models.CharField(
        max_length=30, blank=False, null=False, verbose_name="Фамилия"
    )
    info = models.TextField(
        max_length=350, blank=False, null=False, verbose_name="Краткая информация"
    )
    image = models.ImageField(
        upload_to="chefs_img",
        blank=False,
        null=False,
        verbose_name="Фотография",
        validators=[validate_image_dimensions],
    )

    class Meta:
        db_table = "chefs"
        verbose_name = "Повора"
        verbose_name_plural = "Шеф-поворы"

    def __str__(self):
        return str(self.pk) + " - " + self.name + " " + self.lastName
