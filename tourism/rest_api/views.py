import json
import requests

from rest_framework import viewsets, serializers
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from .serializers import *
from .models import *


'''
Here are all viewsets based on corresponding models that are needed for REST API
'''


class PerevalAddedViewset(viewsets.ModelViewSet):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalAddedSerializer


class PerevalAreasViewset(viewsets.ModelViewSet):
    queryset = PerevalAreas.objects.all()
    serializer_class = PerevalAreasSerializer


class PerevalImagesViewset(viewsets.ModelViewSet):
    queryset = PerevalImages.objects.all()
    serializer_class = PerevalImagesSerializer


class SprActivitiesTypesViewset(viewsets.ModelViewSet):
    queryset = SprActivitiesTypes.objects.all()
    serializer_class = SprActivitiesTypesSerializer


class CoordsViewset(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer


class UsersViewset(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


def submitData(request):                            # base post method for adding passes
    try:
        data = request.body
        data = json.loads(data.decode("utf-8"))     # decoding is needed, because originally its bytes

        # create all instances in DB
        # get or create returns tuple: (object, created -> True, False)
        coords = Coords.objects.get_or_create(
            latitude=data.get('coords').get('latitude'),
            longtitude=data.get('coords').get('longtitude'),
            height=data.get('coords').get('height')
        )

        user = Users.objects.get_or_create(
            name=data.get('user').get('name'),
            fam=data.get('user').get('fam'),
            otc=data.get('user').get('otc'),
            email=data.get('user').get('email'),
            phone=data.get('user').get('phone')
        )

        pereval = PerevalAdded.objects.get_or_create(
            beautyTitle=data.get('beauty_title', "пер. "),
            title=data.get('title'),
            other_titles=data.get('other_titles'),
            connect=data.get('connect'),
            add_time=data.get('add_time'),
            coord_id=coords[0],
            level_winter=data.get('level').get('winter'),
            level_summer=data.get('level').get('summer'),
            level_autumn=data.get('level').get('autumn'),
            level_spring=data.get('level').get('spring'),
            user_id=user[0],
            status='new'
        )

        for image in data.get('images'):
            PerevalImages.objects.get_or_create(
                img=image.get('data'),
                title=image.get('title'),
                pereval_id=pereval[0]
            )

    # catch errors and return corresponding status code
    except ValidationError as e:
        res = {
            'status': 400,
            'message': e,
            'id': None
        }
        return HttpResponse(content=json.dumps(res), status=400)

    except Exception as e:
        res = {
            'status': 500,
            'message': e,
            'id': None
        }
        return HttpResponse(content=json.dumps(res), status=500)
    else:
        res = {
            'status': 200,
            'message': None,
            'id': pereval[0].id
        }
        return HttpResponse(content=json.dumps(res), status=200)
