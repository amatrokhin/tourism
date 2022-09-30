from django.contrib.postgres.fields import ArrayField
from django.db import models


LEVELS = (
    ('1А', '1А'),
    ('1Б', '1Б'),
    ('2А', '2А'),
    ('2Б', '2Б'),
    ('3А', '3А'),
    ('3Б', '3Б')
)

STATUSES = (
    ('new', 'new'),
    ('pending', 'pending'),
    ('accepted', 'accepted'),
    ('rejected', 'rejected')
)


class PerevalAdded(models.Model):                           # ba
    beautyTitle = models.CharField(max_length=50, default='пер. ')
    title = models.CharField(max_length=50)
    other_titles = ArrayField(models.CharField(max_length=50), blank=True)
    connect = ArrayField(models.CharField(max_length=50), blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    add_time = models.DateTimeField()
    coord_id = models.ForeignKey('Coords', null=True, on_delete=models.SET_NULL)
    level_winter = models.CharField(max_length=2, choices=LEVELS, blank=True)
    level_summer = models.CharField(max_length=2, choices=LEVELS, blank=True)
    level_autumn = models.CharField(max_length=2, choices=LEVELS, blank=True)
    level_spring = models.CharField(max_length=2, choices=LEVELS, blank=True)
    user_id = models.ForeignKey('Users', null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=8, choices=STATUSES, default='new')


class PerevalAreas(models.Model):
    title = models.CharField(max_length=50)
    id_parent = models.IntegerField()


class PerevalImages(models.Model):
    img = models.BinaryField()
    title = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    pereval_id = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE)


class SprActivitiesTypes(models.Model):
    title = models.CharField(max_length=50)


class Coords(models.Model):
    latitude = models.FloatField()
    longtitude = models.FloatField()
    height = models.IntegerField()


class Users(models.Model):
    name = models.CharField(max_length=30, blank=True)
    fam = models.CharField(max_length=30, blank=True)
    otc = models.CharField(max_length=30, blank=True)
    email = models.CharField(max_length=50, unique=True)
