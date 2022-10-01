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
    ('new', 'Новое'),
    ('pending', 'В обработке'),
    ('accepted', 'Принято'),
    ('rejected', 'Отклонено')
)


class PerevalAdded(models.Model):                           # basic table for passes
    beautyTitle = models.CharField(max_length=50, default='пер. ')
    title = models.CharField(max_length=50)
    other_titles = models.CharField(max_length=255, null=True)
    connect = models.CharField(max_length=50, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    add_time = models.CharField(max_length=50)
    coords = models.ForeignKey('Coords', null=True, on_delete=models.SET_NULL)
    level_winter = models.CharField(max_length=2, choices=LEVELS, null=True)
    level_summer = models.CharField(max_length=2, choices=LEVELS, null=True)
    level_autumn = models.CharField(max_length=2, choices=LEVELS, null=True)
    level_spring = models.CharField(max_length=2, choices=LEVELS, null=True)
    user = models.ForeignKey('Users', null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=8, choices=STATUSES, default='new')

    def __str__(self):
        return self.beautyTitle + self.title


class PerevalAreas(models.Model):                           # passes areas
    title = models.CharField(max_length=50)
    id_parent = models.IntegerField()


class PerevalImages(models.Model):                          # images of passes
    data = models.BinaryField()
    title = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    pereval = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE)


class SprActivitiesTypes(models.Model):                     # other activities
    title = models.CharField(max_length=50)


class Coords(models.Model):                                 # coordinates of passes
    latitude = models.CharField(max_length=10)
    longtitude = models.CharField(max_length=10)
    height = models.CharField(max_length=10)

    def natural_key(self):                                  # for beautiful serialization
        coords = {
            'latitude': self.latitude,
            'longtitude': self.longtitude,
            'height': self.height
        }
        return coords


class Users(models.Model):                                  # for storing app users in DB
    name = models.CharField(max_length=30, null=True)
    fam = models.CharField(max_length=30, null=True)
    otc = models.CharField(max_length=30, null=True)
    email = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=30, null=True)

    def natural_key(self):                                  # for beautiful serialization
        user = {
            'name': self.name,
            'fam': self.fam,
            'otc': self.otc,
            'email': self.email,
            'phone': self.phone
        }
        return user
