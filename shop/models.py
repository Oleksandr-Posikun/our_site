from django.db import models

# Create your models here.


class Product(models.Model):
    product_name = models.CharField(max_length=30, blank=False)
    price = models.IntegerField(blank=False)
    sale = models.IntegerField(blank=False)
    valuta = models.CharField(max_length=4, blank=False)

    def __str__(self):
        return f"{self.id} {self.product_name} {self.price} {self.sale}"


class Image(models.Model):
    img_path = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f"{self.img_path}"


class ProductPopular(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    img = models.ForeignKey(Image, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.product_name} {self.img.img_path}"


class BestSeller(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    img = models.ForeignKey(Image, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.product_name} {self.img.img_path}"


class StartSliders(models.Model):
    img = models.ForeignKey(Image, on_delete=models.CASCADE)
    position_slider = models.CharField(max_length=50, blank=False)
    position_text = models.CharField(max_length=50)
    active = models.CharField(max_length=7)

    def __str__(self):
        return f"{self.img.img_path} {self.position_slider}"


class StartBanners(models.Model):
    img = models.ForeignKey(Image, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.img.img_path}"


class OfferBanners(models.Model):
    img = models.ForeignKey(Image, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.img.img_path}"


class OurContactsInfo(models.Model):
    telephone = models.CharField(max_length=15)
    email = models.EmailField(max_length=35)
    address = models.CharField(max_length=100)
