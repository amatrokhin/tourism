from .models import *
from rest_framework import serializers


'''
Here are all serializers based on corresponding models that are needed for REST API
'''


class PerevalAddedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PerevalAdded
        fields = ['id', 'beautyTitle', 'title', 'other_titles', 'connect', 'date_added', 'add_time', 'coords', 'level_winter',
                  'level_summer', 'level_autumn', 'level_spring', 'user', 'status']


class PerevalAreasSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PerevalAreas
        fields = ['id', 'title', 'id_parent']


class PerevalImagesSerializer(serializers.HyperlinkedModelSerializer):
    pereval = serializers.StringRelatedField()

    class Meta:
        model = PerevalImages
        fields = ['id', 'data', 'title', 'date_added', 'pereval']


class SprActivitiesTypesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SprActivitiesTypes
        fields = ['id', 'title']


class CoordsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coords
        fields = ['id', 'latitude', 'longtitude', 'height']


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'name', 'fam', 'otc', 'email']
