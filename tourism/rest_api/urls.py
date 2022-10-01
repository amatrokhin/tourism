from django.urls import path
from .views import submitData, get_or_patch_data

urlpatterns = [
    path('submitData/', submitData, name='submit_data'),
    path('submitData/<int:pk>/', get_or_patch_data, name='get_pereval'),
]
