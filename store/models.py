from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100)
    image = models.ImageField(upload_to='product/%Y/%m/%d', blank=True)
    description = models.TextField(max_length=1000, blank=True)
    available = models.BooleanField(default=True)
    popular = models.BooleanField(default=False)
    bestseller = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateField(auto_now_add=True)
    uploaded = models.DateField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f"{self.name}, {self.price}, {self.image}, {self.description}"


class Gallery(models.Model):
    image = models.ImageField(upload_to='product/%Y/%m/%d', blank=True)
    product = models.ForeignKey(
        Product,
        related_name='images',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.image}"
