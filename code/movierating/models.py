from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib import admin


class Category(models.Model):
    categoryName = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return f'{self.categoryName}'


class Movie(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    link = models.TextField(null=True, blank=True)
    duration = models.TextField(null=True, blank=True)
    whoAdded = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name}'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.movie}: {self.user} : {self.rating}'


admin.site.register(Category)
admin.site.register(Movie)
admin.site.register(Review)
