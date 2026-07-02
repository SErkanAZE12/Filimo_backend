from django.contrib import admin
from .models import Actor, Country, Director, Episode, Genre, Movie, Season, Series

# ======================================== #
# تنظیمات عمومی ادمین 
# # ========================================
admin.site.site_header="مدیریت فیلمو"
admin.site.site_title='پنل مدیریت فیلمو'
admin.site.index_title='به پنل مدیریت خوش امدید'

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "slug"]


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "slug"]


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ["title", "year", "rating", "language", "is_featured"]
    list_filter = ["language", "rating", "country", "genres"]
    search_fields = ["title", "description"]


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ["title", "year", "rating", "language", "is_featured"]
    list_filter = ["language", "rating", "country", "genres"]
    search_fields = ["title", "description"]


admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Episode)
admin.site.register(Season)
