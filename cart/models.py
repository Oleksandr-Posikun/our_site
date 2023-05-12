from django.db import models

from store.models import Product


# Create your models here.


class UserCart(models.Model):
    user = models.CharField(max_length=100, db_index=True)
    product = models.ForeignKey(
        Product,
        related_name='user_carts',
        on_delete=models.CASCADE
    )
    count = models.IntegerField()
    created = models.DateField(auto_now_add=True)
    uploaded = models.DateField(auto_now=True)

    class Meta:
        ordering = ('user',)

    def __str__(self):
        return f"{self.user}, {self.product}, {self.count}, {self.created}"
