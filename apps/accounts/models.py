from django.contrib.auth.models import User


class ShopUser(User):

    class Meta:
        proxy = True
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"

    def orders(self):
        return self.orders.all()
