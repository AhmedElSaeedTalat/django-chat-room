from django.urls import path
from . import views
urlpatterns = [
    path('<room_name>/', views.room)
]