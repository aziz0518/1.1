from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    published_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def clean(self):
        # Validate title length
        if len(self.title) < 3:
            raise ValidationError("Title must be at least 3 characters long.")

        # Validate price
        if self.price < 0:
            raise ValidationError("Price must be 0.00 or higher.")

        # Validate published_date after author's birth_date
        if self.author and self.published_date < self.author.birth_date:
            raise ValidationError("Published date must be after the author's birth date.")

    def __str__(self):
        return self.title
