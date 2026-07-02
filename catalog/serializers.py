from rest_framework import serializers
from .models import Genre, Country, Actor, Director, Movie, Series, Season, Episode


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name", "slug"]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name", "slug"]


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["id", "name", "image"]


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ["id", "name", "image"]


class MovieListSerializer(serializers.ModelSerializer):
    """
    سریالایزر لیست فیلم‌ها - برای MovieSlider.js و HomePage
    خروجی دقیقاً مشابه filiter.json
    """

    genre = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    country = serializers.CharField(source="country.name", read_only=True)
    image = serializers.ImageField(source="thumbnail", read_only=True)
    year = serializers.CharField(read_only=True)
    rating = serializers.CharField(read_only=True)
    language = serializers.CharField(read_only=True)
    agerating = serializers.CharField(source="age_rate", read_only=True)
    production = serializers.IntegerField(source="year", read_only=True)

    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "slug",
            "image",
            "year",
            "rating",
            "category",
            "language",
            "agerating",
            "country",
            "genre",
            "production",
        ]

    def get_genre(self, obj):
        first_genre = obj.genres.first()
        return first_genre.slug if first_genre else ""

    def get_category(self, obj):
        return "movie"


class MovieDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    country = CountrySerializer(read_only=True)
    director = DirectorSerializer(many=True, read_only=True, source="director")
    actors = ActorSerializer(many=True, read_only=True)

    category = serializers.SerializerMethodField()
    language = serializers.CharField(read_only=True)
    agerating = serializers.CharField(source="age_rating", read_only=True)
    production = serializers.IntegerField(source="year", read_only=True)

    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "duration",
            "thumbnail",
            "video",
            "genres",
            "country",
            "director",
            "actors",
            "is_trending",
            "is_featured",
            "language",
            "agerating",
            "year",
            "category",
            "created_at",
            "production",
        ]

    def get_category(self, obj):
        return "movie"


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ["id", "title", "video_url", "duration", "number"]


class SeasonSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True, read_only=True)

    class Meta:
        model = Season
        fields = ["id", "title", "number", "episodes"]


class SeriesListSerializer(serializers.ModelSerializer):

    genre = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    country = serializers.CharField(source="country.name", read_only=True)
    image = serializers.ImageField(source="thumbnail", read_only=True)
    rating = serializers.CharField(read_only=True)
    filmlanguage = serializers.CharField(source="language", read_only=True)
    ageRating = serializers.CharField(source="age_rating", read_only=True)
    category = serializers.SerializerMethodField()
    productionYear = serializers.SerializerMethodField()

    class Meta:
        model = Series
        fields = [
            "id",
            "title",
            "slug",
            "image",
            "year",
            "rating",
            "category",
            "filmlanguage",
            "ageRating",
            "country",
            "genre",
            "productionYear",
        ]

    def get_genre(self, obj):
        first_genre = obj.genres.first()
        return first_genre.slug if first_genre else ""

    def get_category(self, obj):
        return "series"

    def get_year(self, obj):
        if hasattr(obj, "year") and obj.year:
            return str(obj.year)

        first_season = obj.seasons.first()
        if first_season:
            return str(first_season.created_at.year)
        return ""

    def get_productionYear(self, obj):
        if hasattr(obj, "year") and obj.year:
            return obj.year
        first_season = obj.seasons.first()
        if first_season:
            return first_season.created_at.year
        return obj.created_at.year


class SeriesDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    country = CountrySerializer(read_only=True)
    directors = DirectorSerializer(many=True, read_only=True, source="director")
    seasons = SeasonSerializer(many=True, read_only=True)

    filmLanguage = serializers.CharField(source="language", read_only=True)
    ageRating = serializers.CharField(source="age_rate", read_only=True)
    category = serializers.SerializerMethodField()

    class Meta:
        model = Series
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "thumbnail",
            "genres",
            "country",
            "directors",
            "seasons",
            "is_trending",
            "is_featured",
            "filmLanguage",
            "ageRating",
            "category",
            "created_at",
        ]

    def get_category(self, obj):
        return "series"


class SliderSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    filmLanguage = serializers.CharField(source="language", read_only=True)
    ageRating = serializers.CharField(source="age_rating", read_only=True)
    description = serializers.CharField(read_only=True)
    productionYear = serializers.IntegerField(source="year", read_only=True)
    country = serializers.CharField(source="country.name", read_only=True)

    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "description",
            "image",
            "filmLanguage",
            "ageRating",
            "country",
            "genre",
            "productionYear",
            "category",
            "price",
            "link",
        ]

    def get_category(self, obj):
        return "movie"

    def get_image(self, obj):
        if obj.banner and hasattr(obj.banner, "url"):
            return obj.banner.url
        elif obj.thumbnail and hasattr(obj.thumbnail, "url"):
            return obj.thumbnail.url
        return None

    def get_genre(self, obj):
        first_genre = obj.genres.first()
        return first_genre.slug if first_genre else " "

    def get_link(self, obj):
        return f"/product/{obj.id}"

    def get_price(self, obj):
        # فعلاً قیمت پیش‌فرض - بعداً می‌توانیم به مدل اضافه کنیم
        return "250,000 تومان"
