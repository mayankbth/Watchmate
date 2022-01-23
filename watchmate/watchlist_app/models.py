from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name


class WatchList(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name="watchlist")
    active = models.BooleanField(default=True)
    # we are referring this active as if series or movie is released or launched or something else.
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# this is going to be one to many relationship. That is, one movie can have multiple reviews but one review can only
# have one movie
class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    # rating is between one to five
    # i am adding validators here. it will helps us to define a specific gap or to define a specific range for numbers.
    # here i am using min value and max value validators.
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name='reviews')
    # https://stackoverflow.com/questions/2642613/what-is-related-name-used-for-in-django

    # if we find fake review, we can turn this active into false.
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    # auto_now - updates the value of field to current time and date every time the Model.save() is called.
    # auto_now_add - updates the value with the time and date of creation of record.

    def __str__(self):
        return str(self.rating) + " | " + self.watchlist.title + " | " + str(self.review_user)
        # here we are converting "self.rating" to string because if we don't then we will get the error
        # "__str__ returned non-string (type int)"
        # and also performing concatenation to return rating with the movie name


# class Movie(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.CharField(max_length=200)
#     active = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.name
