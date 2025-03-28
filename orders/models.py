from django.core.validators import RegexValidator
from django.db import models
from main.models import Products
from users.models import User


class OrderitemQuerySet(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


# Таблица заказов пользователя
class Order(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_DEFAULT,
        blank=True,
        null=True,
        verbose_name="Пользователь",
        default=None,
    )
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания заказа"
    )
    phone_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^\+7\s\(\d{3}\)\s\d{3}-\d{2}-\d{2}$",  # Example regex for international phone numbers
                message="Номер телефона должен быть в формате: '+7 (***) ***-**-**'.",
            )
        ],
        verbose_name="Номер телефона",
    )
    # requires_delivery = models.BooleanField(
    #     default=False, verbose_name="Требуется доставка"
    # )
    # delivery_address = models.TextField(
    #     null=True, blank=True, verbose_name="Адрес доставки"
    # )
    payment_on_get = models.BooleanField(
        default=False, verbose_name="Оплата при получении"
    )
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    status = models.CharField(
        max_length=50, default="В обработке", verbose_name="Статус заказа"
    )

    def total_price(self):
        # Суммируем стоимость всех товаров, связанных с заказом
        return sum(
            item.price * item.quantity for item in self.orderitem_set.all()
        )

    class Meta:
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ("id",)

    def __str__(self):
        return f"Заказ № {self.pk} | Покупатель: {self.user.username} - {self.user.first_name} {self.user.last_name}"

# Перечень заказов пользователя
class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(
        to=Products,
        on_delete=models.SET_DEFAULT,
        null=True,
        verbose_name="Продукт",
        default=None,
    )
    name = models.CharField(max_length=150, verbose_name="Название")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата продажи"
    )

    class Meta:
        db_table = "order_item"
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданные товары"
        ordering = ("id",)

    objects = OrderitemQuerySet.as_manager()

    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

    def __str__(self):
        return f"Товар {self.name} | Заказ № {self.order.pk}"
