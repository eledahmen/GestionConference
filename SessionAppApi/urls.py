from .views import SessionViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path,include
router= DefaultRouter()
router.register('session',SessionViewSet,basename='session')
urlpatterns=[
    path('',include(router.urls))
]