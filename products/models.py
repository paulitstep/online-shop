from django.db import models
from django.db.models import Q

BOOK_CATEGORY_CHOICES = (
    ('russian', 'Русская классическая литература'),
    ('foreign', 'Зарубежная классическая литература'),
    ('detective', 'Детектив'),
    ('fantasy', 'Фантастика, фэнтези'),
)


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def search(self, query):
        lookups = (Q(title__icontains=query) |
                   Q(author_year__icontains=query)
                   )
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()

    def search(self, query):
        return self.get_queryset().active().search(query)


class Product(models.Model):
    category = models.CharField(max_length=250, blank=True, null=True, choices=BOOK_CATEGORY_CHOICES)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    title = models.CharField(max_length=150)
    author_year = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True, unique=True)

    objects = ProductManager()

    def get_absolute_url(self):
        return f'/products/{self.slug}/'

    def __str__(self):
        return self.title
