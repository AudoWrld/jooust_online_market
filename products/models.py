from django.db import models
from django.conf import settings


class Product(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, null=True, blank=True)
    buying_price = models.IntegerField(
        help_text="This field will help to calculate profits"
    )
    selling_price = models.IntegerField()
    discount_price = models.IntegerField(
        help_text="This amount will appear to subscribed users"
    )
    quantity = models.IntegerField(default=1)
    product_image = models.ImageField(upload_to="product_display_image/")

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="product_images/")

    def __str__(self):
        return f"Image for {self.product.name}"
