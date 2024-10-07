from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils import timezone


# Create your models here.
class Products(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # stripe_id = models.CharField(max_length=120, blank=True, null=True)
    name = models.CharField(max_length=120)
    handle = models.SlugField(max_length=120, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=9.99)
    og_price = models.DecimalField(max_digits=5, decimal_places=2, default=9.99)
    stripe_price = models.IntegerField(default=999)
    price_changed_timestamp = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/products/{self.handle}/"

    def save(self, *args, **kwargs):
        if not self.handle:
            base_slug = slugify(self.name)
            slug = base_slug
            num = 1
            while Products.objects.filter(handle=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.handle = slug
        if self.price != self.og_price:
            # * price changed
            self.og_price = self.price
            #! trigger api request to stripe

            self.stripe_price = int(self.price * 100)
            self.price_changed_timestamp = timezone.now()
        super().save(*args, **kwargs)
