from django.urls import path
from . import views

urlpatterns = [
   
   	path('<str:username>',views.profile_detail_api_view),
]