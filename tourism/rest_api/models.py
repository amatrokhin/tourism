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


class PerevalAdded(models.Model):                           # basic table for passes
    beautyTitle = models.CharField(max_length=50, default='пер. ')
    title = models.CharField(max_length=50)
    other_titles = models.CharField(max_length=255, null=True)
    connect = models.CharField(max_length=50, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    add_time = models.CharField(max_length=50)
    coord_id = models.ForeignKey('Coords', null=True, on_delete=models.SET_NULL)
    level_winter = models.CharField(max_length=2, choices=LEVELS, null=True)
    level_summer = models.CharField(max_length=2, choices=LEVELS, null=True)
    level_autumn = models.CharField(max_length=2, choices=LEVELS, null=True)
    level_spring = models.CharField(max_length=2, choices=LEVELS, null=True)
    user_id = models.ForeignKey('Users', null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=8, choices=STATUSES, default='new')

    def __str__(self):
        return self.beautyTitle + self.title


class PerevalAreas(models.Model):                           # passes areas
    title = models.CharField(max_length=50)
    id_parent = models.IntegerField()


class PerevalImages(models.Model):                          # images of passes
    img = models.BinaryField()
    title = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    pereval_id = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE)


class SprActivitiesTypes(models.Model):                     # other activities
    title = models.CharField(max_length=50)


class Coords(models.Model):                                 # coordinates of passes
    latitude = models.CharField(max_length=10)
    longtitude = models.CharField(max_length=10)
    height = models.CharField(max_length=10)


class Users(models.Model):                                  # for storing app users in DB
    name = models.CharField(max_length=30, null=True)
    fam = models.CharField(max_length=30, null=True)
    otc = models.CharField(max_length=30, null=True)
    email = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=30, null=True)
