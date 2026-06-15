from django.db import models
from common.models import BaseModel
from django.utils.text import slugify


class Genre(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name


class Actor(BaseModel):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to="actors/", null=True, blank=True)

    def __str__(self):
        return self.name


class Director(BaseModel):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to="actors/", null=True, blank=True)

    def __str__(self):
        return self.name


class Movie(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    year = models.ImageField()
    duration = models.IntegerField(help_text="minutes")
    thumbnail = models.ImageField(upload_to="movies/")
    video = models.URLField()
    genres = models.ManyToManyField(Genre, related_name="movies")
    director = models.ManyToManyField(Director, related_name="movies")
    actors = models.ManyToManyField(Actor, related_name="movies")
    is_trending = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Series(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="movies/")
    genres = models.ManyToManyField(Genre, related_name="movies")
    director = models.ManyToManyField(Director, related_name="movies")
    is_trending = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Season(BaseModel):
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name="season")
    title = models.CharField(max_length=255, blank=True)
    number = models.IntegerField()

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

    def __str__(self):
        return f"{self.season} Ep {self.number}"
