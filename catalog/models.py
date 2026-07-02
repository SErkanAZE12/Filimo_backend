from django.db import models
from common.models import BaseModel
from django.utils.text import slugify


class Genre(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Country(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Actor(BaseModel):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to="actors/", null=True, blank=True)

    class Meta:

        verbose_name = "Actor"
        verbose_name_plural = "Actors"

    def __str__(self):
        return self.name


class Director(BaseModel):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to="directors/", null=True, blank=True)

    class Meta:
        verbose_name = "Director"
        verbose_name_plural = "Directors"

    def __str__(self):
        return self.name


class Movie(BaseModel):
    LANGUAGE_CHOICES = [
        ("farsi", "فارسی (دوبله)"),
        ("subtitle", "زیرنویس فارسی"),
        ("english", "زیرنویس انگلیسی"),
        ("original", "زبان اصلی"),
        ("multi", "چند زبانه"),
    ]

    AGE_RATING_CHOICES = [
        ("all", "همه سنین"),
        ("12+", "۱۲+"),
        ("13+", "۱۳+"),
        ("15+", "۱۵+"),
        ("18+", "۱۸+"),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    year = models.IntegerField()
    duration = models.IntegerField(help_text="minutes")
    rating = models.FloatField(default=0.0)
    banner = models.ImageField(upload_to="movies/banners", null=True)
    thumbnail = models.ImageField(upload_to="movies/thumbnail", null=True, blank=True)
    language = models.CharField(
        max_length=20, choices=LANGUAGE_CHOICES, default="english"
    )

    age_rating = models.CharField(max_length=5, choices=AGE_RATING_CHOICES, default="all",db_column='age_rate')
    video = models.URLField(null=True, blank=True)

    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    genres = models.ManyToManyField(Genre, related_name="movies")
    directors = models.ManyToManyField(Director, related_name="movies")
    actors = models.ManyToManyField(Actor, related_name="movies")
    is_trending = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        ordering = ["-year", "-id"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Series(BaseModel):
    languages = Movie.LANGUAGE_CHOICES
    Age_rate = Movie.AGE_RATING_CHOICES
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="Series/", null=True, blank=True)
    banner = models.ImageField(upload_to="Series/banners", null=True)
    language = models.CharField(max_length=20, choices=languages, default="english")
    year = models.IntegerField(null=True,blank=True)
    rating = models.FloatField(default=0.0)
    age_rating = models.CharField(max_length=5, choices=Age_rate, default="all")
    actors = models.ManyToManyField(Actor, related_name="series")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    genres = models.ManyToManyField(Genre, related_name="series")
    directors = models.ManyToManyField(Director, related_name="series")
    is_trending = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Series"
        verbose_name_plural = "Series"
        ordering = ["-year", "-id"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Season(BaseModel):
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name="seasons")
    title = models.CharField(max_length=255, blank=True)
    number = models.IntegerField()

    class Meta:
        verbose_name = "Season"
        verbose_name_plural = "Seasons"
        unique_together = ["series", "number"]
        ordering = ["number"]

    def __str__(self):
        return f"{self.series.title} season{self.number}"


class Episode(BaseModel):
    season = models.ForeignKey(
        Season, on_delete=models.CASCADE, related_name="episodes"
    )
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    duration = models.IntegerField()
    number = models.IntegerField()

    class Meta:
        verbose_name = "episode"
        verbose_name_plural = "episodes"
        ordering = ["number"]
        unique_together = ["season", "number"]

    def __str__(self):
        return f"{self.season} Ep {self.number}"
