from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from main.api import views

urlpatterns = [
	path('', views.api_routes),
	path('list/', views.record_list),
	path('create/', views.record_create),
	path('read/<int:pk>', views.record_detail),
	path('modify/<int:pk>', views.record_modify),
	path('remove/<int:pk>', views.record_delete),
]

urlpatterns = format_suffix_patterns(urlpatterns)