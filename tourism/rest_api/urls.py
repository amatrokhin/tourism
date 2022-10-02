from django.urls import path
from django.views.generic import TemplateView

from .views import submitData, get_or_patch_data

urlpatterns = [
    path('submitData/', submitData, name='submit_data'),
    path('submitData/<int:pk>/', get_or_patch_data, name='get_pereval'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
]
