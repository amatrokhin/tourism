from django.urls import path
from .views import submitData


urlpatterns = [
    path('pereval_add/', submitData, name='submit_data'),
]