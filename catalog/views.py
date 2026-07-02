from django.shortcuts import render
from rest_framework import viewsets, filters, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from catalog.models import Actor, Country, Genre, Movie, Season, Director, Series
from catalog.serializers import (
    ActorSerializer,
    CountrySerializer,
    DirectorSerializer,
    GenreSerializer,
    MovieDetailSerializer,
    MovieListSerializer,
    SeriesDetailSerializer,
    SliderSerializer,
    SeriesListSerializer,
)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = "slug"


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.all()

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = {
        "genres__slug": ["exact"],
        "country__slug": ["exact"],
        "language": ["exact"],
        "age_rating": ["exact"],
        "is_featured": ["exact"],
        "is_trending": ["exact"],
    }
    search_fields = ["title", "description"]
    ordering_fields = ["year", "rating", "created_at"]
    ordering = ["-year"]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "list":
            return MovieListSerializer
        return MovieDetailSerializer

    @action(detail=False, methods=["get"])
    def featured(self, request):
        featured_movies = self.queryset.filter(is_featured=True)[:10]
        serializer = SliderSerializer(featured_movies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def trending(self, request):
        """
        فیلم‌های پرطرفدار
        GET /api/movies/trending/
        """
        trending_movies = self.queryset.filter(is_trending=True)[:20]
        serializer = MovieListSerializer(trending_movies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="by-genre/(?P<genre_slug>[^/.]+)")
    def by_genre(self, request, genre_slug=None):
        """
        فیلم‌ها بر اساس ژانر - برای HomePage sections
        GET /api/movies/by-genre/comedy/
        GET /api/movies/by-genre/action/
        """
        movies = self.queryset.filter(genre__slug=genre_slug).distinct()[:15]
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)


class SeriesViewSet(viewsets.ReadOnlyModelViewSet):
    """مدیریت سریال‌ها - مشابه MovieViewSet
    GET /api/series/
    GET /api/series/?genre=drama
    GET /api/series/{slug}/"""

    queryset = Series.objects.all().prefetch_related(
        "genres", "country", "directors", "seasons__episodes"
    )
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = {
        "genres__slug": ["exact"],
        "country__slug": ["exact"],
        "language": ["exact"],
        "age_rating": ["exact"],
        "is_featured": ["exact"],
        "is_trending": ["exact"],
    }

    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "list":
            return SeriesListSerializer
        return SeriesDetailSerializer

    @action(detail=False, methods=["get"])
    def featured(self, request):
        featured_serial = self.queryset.filter(is_featured=True)[:15]
        serializer = SeriesListSerializer(featured_serial, many=True)
        return Response(serializer.data)


class SliderViewSet(viewsets.ViewSet):
    """اسلایدر اصلی صفحه خانه
    GET /api/slider/
    ترکیبی از فیلم‌ها و سریال‌های ویژه که banner دارند"""

    def list(self, request):
        # فیلم های ویژه با banner
        featured_movies = (
            Movie.objects.filter(is_featured=True)
            .filter(Q(banner__isnull=False) | Q(thumbnail__isnull=False))
            .select_related("country")
            .prefetch_related("genres")[:5]
        )

        # سریال های ویژه با  banner
        featured_serial = (
            Series.objects.filter(is_featured=True)
            .filter(Q(banner__isnull=False)| Q(thumbnail__isnull=False))
            .select_related("country")
            .select_related("country")
            .prefetch_related("genres")[:5]
        )
        # suffle
        all_featured = list(featured_movies) + list(featured_serial)
        serializer = SliderSerializer(all_featured[:10], many=True)
        return Response(serializer.data)
