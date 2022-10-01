from django.urls import path
from .views import submitData, get_or_patch_data, get_user_pervals_list


urlpatterns = [
    path('submitData/', submitData, name='submit_data'),
    path('submitData/<int:pk>/', get_or_patch_data, name='get_pereval'),
]
