import json

from rest_framework import viewsets
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize

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


@csrf_exempt
def submitData(request):                            # base post method for adding passes and get for returning them
    try:
        # if GET method, then return list with parameters, specifically authors passes
        if request.method == 'GET':
            perevals = PerevalAdded.objects.filter(user__email=request.GET['user__email'])

            # use natural key to serialize fields of coords
            data = serialize('json', perevals, use_natural_foreign_keys=True)

            return HttpResponse(content=data, status=200)

        # if POST method, then create a new pass
        elif request.method == 'POST':
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
                beautyTitle=data.get('beauty_title', 'пер. '),
                title=data.get('title'),
                other_titles=data.get('other_titles'),
                connect=data.get('connect'),
                add_time=data.get('add_time'),
                coords=coords[0],
                level_winter=data.get('level').get('winter'),
                level_summer=data.get('level').get('summer'),
                level_autumn=data.get('level').get('autumn'),
                level_spring=data.get('level').get('spring'),
                user=user[0],
                status='new'
            )

            for image in data.get('images'):
                PerevalImages.objects.get_or_create(
                    img=image.get('data'),
                    title=image.get('title'),
                    pereval=pereval[0]
                )

    # catch errors and return corresponding status code
    except ValidationError:
        res = {
            'status': 400,
            'message': 'Не хватает полей или поля заполнены некорректно',
            'id': None
        }
        return HttpResponse(content=json.dumps(res, ensure_ascii=False), status=400)

    except Exception:
        res = {
            'status': 500,
            'message': 'Ошибка подключения к базе данных',
            'id': None
        }
        return HttpResponse(content=json.dumps(res, ensure_ascii=False), status=500)

    else:
        res = {
            'status': 200,
            'message': None,
            'id': pereval[0].id
        }
        return HttpResponse(content=json.dumps(res, ensure_ascii=False), status=200)


@csrf_exempt
def get_or_patch_data(request, pk):                 # get or patch data if status == 'new'
    try:
        if request.method == 'GET':
            data = serialize('json', [PerevalAdded.objects.get(pk=pk)], use_natural_foreign_keys=True)
            return HttpResponse(content=data, status=200)

        elif request.method == 'PATCH':
            data = request.body
            data = json.loads(data.decode('utf-8'))

            pereval = PerevalAdded.objects.select_related('coords').get(pk=pk)

            # only alter passes with status new
            if pereval.status != 'new':
                res = {
                    'state': 0,
                    'message': 'Нельзя изменить перевалы, у которых статус отличен от "Новое"'
                }
                return HttpResponse(content=json.dumps(res, ensure_ascii=False), status=400)

            # alter neccessary fields, if not in request then leave the same
            if new_coords := data.get('coords'):
                old_coords = Coords.objects.get(pk=pereval.coords.id)

                old_coords.longtitude = new_coords.get('longtitude', old_coords.longtitude)
                old_coords.latitude = new_coords.get('latitude', old_coords.latitude)
                old_coords.height = new_coords.get('height', old_coords.height)

                old_coords.save()

            if new_images := data.get('images'):
                old_images = Coords.objects.filter(pereval=pereval)

                for i, elem in enumerate(old_images):
                    if i <= len(new_images):
                        elem.data = new_images.get('data', elem.data)
                        elem.title = new_images.get('title', elem.title)
                        elem.date_added = new_images.get('date_added', elem.date_added)

                        elem.save()

                    # if less images in request then is in DB delete extra
                    else:
                        elem.delete()

            pereval.beautyTitle = data.get('beauty_title', pereval.beautyTitle)
            pereval.title = data.get('title', pereval.title)
            pereval.other_titles = data.get('other_titles', pereval.other_titles)
            pereval.connect = data.get('connect', pereval.connect)
            pereval.add_time = data.get('add_time', pereval.add_time)
            pereval.date_added = data.get('date_added', pereval.date_added)
            pereval.level_winter = data.get('level_winter', pereval.level_winter)
            pereval.level_summer = data.get('level_summer', pereval.level_summer)
            pereval.level_autumn = data.get('level_autumn', pereval.level_autumn)
            pereval.level_spring = data.get('level_spring', pereval.level_spring)

            pereval.save()

    # if error or success write corresponding message
    except ValidationError:                         # check for correctness
        res = {
            'state': 0,
            'message': 'Поля заполнены некорректно'
        }
        return HttpResponse(content=json.dumps(res, ensure_ascii=False), status=400)

    except Exception:                               # mainly DB errors
        res = {
            'state': 0,
            'message': 'Ошибка подключения к базе данных'
        }
        return HttpResponse(content=json.dumps(res, ensure_ascii=False), status=500)

    else:
        res = {
            'state': 1,
            'message': 'Все норм'
        }
        return HttpResponse(content=json.dumps(res, ensure_ascii=False), status=200)
