from django.db import models
from django.utils.html import format_html

from main.models import Products
from users.models import User


#  ''' Считаем общее кол-во товаров и их стоимость '''
class CartQuerySet(models.QuerySet):
    # Полная стоимость всех корзин покупателя
    def total_price(self):
        return sum(cart.products_price() for cart in self)

    # Общее кол-во товаров в корзинах
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


# Модель корзины товаров
class Cart(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Пользователь",
    )
    session_key = models.CharField(
        max_length=32, blank=True, null=True, verbose_name="Ключ сессии"
    )
    product = models.ForeignKey(
        to=Products, on_delete=models.CASCADE, verbose_name="Продукт"
    )
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name="Количество")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        db_table = "carts"
        verbose_name = "Корзину"
        verbose_name_plural = "Корзины"

    objects = CartQuerySet().as_manager()

    # Метод для отображения миниатюры в админке
    def image_tag(self):
        if self.product.image:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', self.product.image.url)
        return "Нет изображения"
    image_tag.short_description = "Миниатюра"

    # Цена общего кол-ва товаров
    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

    def __str__(self):
        if self.user:
            return f"Корзина: {self.user.username} | Товар: {self.product.name} | Кол-во: {self.quantity}"
        return f"Анонимная корзина | Товар: {self.product.name} | Кол-во: {self.quantity}"
