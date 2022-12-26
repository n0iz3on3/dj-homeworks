from django.db import models
from django.utils.text import slugify


class Phone(models.Model):
    name = models.CharField(max_length=50)
    image = models.URLField(max_length=300)
    price = models.DecimalField(max_digits=7, decimal_places=1)
    release_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = models.SlugField(editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Phone, self).save(*args, **kwargs)