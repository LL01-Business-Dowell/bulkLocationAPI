from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('get-local-nearby-v3/', views.GetNearbyPlacesLocallyV3.as_view()),
    path('get-details-list-stage1/', views.GetPlaceDetailsListStage1.as_view()),
]
