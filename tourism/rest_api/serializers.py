from .models import *
from rest_framework import serializers


class PerevalAddedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PerevalAdded
        fields = ['id', 'beautyTitle', 'title', 'other_titles', 'connect', 'date_added', 'add_time', 'coord_id', 'level_winter',
                  'level_summer', 'level_autumn', 'level_spring', 'user_id', 'status']


class PerevalAreasSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PerevalAreas
        fields = ['id', 'title', 'id_parent']


class PerevalImagesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PerevalImages
        fields = ['id', 'img', 'title', 'date_added', 'pereval_id']


class SprActivitiesTypesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = ['id', 'title']


class CoordsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = ['id', 'latitude', 'longtitude', 'height']


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = ['id', 'name', 'fam', 'otc', 'email']
