from django.db import models
from register.models import User
from products.models import product


# Create your models here.
class order(models.Model):
    user_id = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    pay_time = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.user_id)


class order_details(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    order = models.ForeignKey(order, on_delete=models.CASCADE)
    final_price = models.IntegerField(null=True, blank=True)
    countp = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.order)
