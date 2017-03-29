from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class ShopUser(User):

    class Meta:
        proxy = True
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def orders(self):
        return self.orders.all()
