import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from catalog.models import Genre, Country, Movie, Series


class Command(BaseCommand):
    help = 'Import movie and series data from JSON files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before import',
        )

    def handle(self, *args, **options):
        base_dir = settings.BASE_DIR
        
        if options['clear']:
            self.stdout.write(self.style.WARNING('🗑️  Clearing existing data...'))
            Movie.objects.all().delete()
            Series.objects.all().delete()
            Genre.objects.all().delete()
            Country.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✅ Data cleared successfully'))

        # ===== Import Genres =====
        self.stdout.write('\n📂 Importing genres...')
        genres_json = [
            {'name': 'اکشن', 'slug': 'action'},
            {'name': 'درام', 'slug': 'drama'},
            {'name': 'کمدی', 'slug': 'comedy'},
            {'name': 'ترسناک', 'slug': 'horror'},
            {'name': 'عاشقانه', 'slug': 'romance'},
            {'name': 'جنایی', 'slug': 'crime'},
            {'name': 'علمی تخیلی', 'slug': 'sci-fi'},
            {'name': 'ماجراجویی', 'slug': 'adventure'},
            {'name': 'انیمیشن', 'slug': 'animation'},
            {'name': 'مستند', 'slug': 'documentary'},
            {'name': 'تاریخی', 'slug': 'history'},
            {'name': 'جنگی', 'slug': 'war'},
            {'name': 'خانوادگی', 'slug': 'family'},
            {'name': 'فانتزی', 'slug': 'fantasy'},
        ]
        
        genre_map = {}
        for g in genres_json:
            genre, _ = Genre.objects.get_or_create(slug=g['slug'], defaults={'name': g['name']})
            genre_map[g['slug']] = genre
            self.stdout.write(f'  ✓ Genre: {genre.name}')

        # ===== Import Countries =====
        self.stdout.write('\n🌍 Importing countries...')
        countries_json = [
            {'name': 'ایران', 'slug': 'iran'},
            {'name': 'آمریکا', 'slug': 'usa'},
            {'name': 'انگلستان', 'slug': 'uk'},
            {'name': 'کره جنوبی', 'slug': 'korea'},
            {'name': 'فرانسه', 'slug': 'france'},
            {'name': 'هند', 'slug': 'india'},
            {'name': 'ژاپن', 'slug': 'japan'},
            {'name': 'آلمان', 'slug': 'germany'},
        ]
        
        country_map = {}
        for c in countries_json:
            country, _ = Country.objects.get_or_create(slug=c['slug'], defaults={'name': c['name']})
            country_map[c['slug']] = country
            self.stdout.write(f'  ✓ Country: {country.name}')

        # ===== Import Movies from filiter.json =====
        self.stdout.write('\n🎬 Importing movies and series...')
        filiter_path = base_dir / 'data' / 'filiter.json'
        
        if not filiter_path.exists():
            self.stdout.write(self.style.ERROR(f'❌ File {filiter_path} not found!'))
            return
        
        with open(filiter_path, 'r', encoding='utf-8') as f:
            movies_data = json.load(f)

        movies_count = 0
        series_count = 0
        
        for item in movies_data:
            category = item.get('category', 'movie')
            genre_slug = item.get('genre', 'drama')
            country_slug = item.get('country', 'iran')
            language = item.get('filmLanguage', 'english')
            
            # ✅ اصلاح: ageRating → age_rate
            age_rate = item.get('ageRating', 'all')
            
            try:
                year = int(item.get('year', 2024))
            except (ValueError, TypeError):
                year = 2024
            
            try:
                rating = float(item.get('rating', 0))
            except (ValueError, TypeError):
                rating = 0.0
            
            if category == 'movie':
                movie, created = Movie.objects.get_or_create(
                    slug=f"movie-{item.get('id')}",
                    defaults={
                        'title': item.get('title', 'Untitled'),
                        'description': f"Movie {item.get('title', '')}",
                        'year': year,
                        'duration': 120,
                        'rating': rating,
                        'language': language,
                        'age_rate': age_rate,  # ✅ اصلاح شد
                        'country': country_map.get(country_slug),
                        'is_trending': True,
                        'is_featured': item.get('id', 0) <= 5,
                    }
                )
                if created:
                    movie.genres.add(genre_map.get(genre_slug))
                    movies_count += 1
                    self.stdout.write(f'  🎥 Movie added: {movie.title}')
                    
            elif category == 'series':
                series, created = Series.objects.get_or_create(
                    slug=f"series-{item.get('id')}",
                    defaults={
                        'title': item.get('title', 'Untitled'),
                        'description': f"Series {item.get('title', '')}",
                        'year': year,
                        'rating': rating,
                        'language': language,
                        'age_rate': age_rate,  # ✅ اصلاح شد
                        'country': country_map.get(country_slug),
                        'is_trending': True,
                        'is_featured': item.get('id', 0) <= 5,
                    }
                )
                if created:
                    series.genres.add(genre_map.get(genre_slug))
                    series_count += 1
                    self.stdout.write(f'  📺 Series added: {series.title}')

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Data import completed!\n'
            f'   🎥 Movies: {movies_count}\n'
            f'   📺 Series: {series_count}\n'
            f'   🎭 Genres: {len(genre_map)}\n'
            f'   🌍 Countries: {len(country_map)}'
        ))