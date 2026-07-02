from django.urls import path, include
from rest_framework.routers import DefaultRouter
from catalog.views import (
    GenreViewSet,
    CountryViewSet,
    MovieViewSet,
    SliderViewSet,
    SliderViewSet,
)

# create router for viewsets
router = DefaultRouter()
router.register(r"genres", GenreViewSet, basename="genre")
router.register(r"country", CountryViewSet, basename="country")
router.register(r"movies", MovieViewSet, basename="movies")
router.register(r"series", SliderViewSet, basename="series")
router.register(r"slider", SliderViewSet, basename="slider")


urlpatterns = [
    path('',include(router.urls))
]

