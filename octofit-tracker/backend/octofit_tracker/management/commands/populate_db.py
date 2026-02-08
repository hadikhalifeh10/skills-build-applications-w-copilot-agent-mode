from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import connection
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Deleting existing data...')
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        self.stdout.write('Creating test teams...')
        marvel = Team.objects.create(name='Marvel', description='Marvel superheroes team')
        dc = Team.objects.create(name='DC', description='DC superheroes team')

        self.stdout.write('Creating test users...')
        users = [
            User.objects.create(name='Iron Man', email='ironman@marvel.com', team='Marvel', is_superhero=True),
            User.objects.create(name='Captain America', email='cap@marvel.com', team='Marvel', is_superhero=True),
            User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team='Marvel', is_superhero=True),
            User.objects.create(name='Batman', email='batman@dc.com', team='DC', is_superhero=True),
            User.objects.create(name='Superman', email='superman@dc.com', team='DC', is_superhero=True),
            User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team='DC', is_superhero=True),
        ]

        self.stdout.write('Creating test activities...')
        from datetime import date
        for user in users:
            Activity.objects.create(user=user, type='Running', duration=30, date=date.today())
            Activity.objects.create(user=user, type='Cycling', duration=45, date=date.today())

        self.stdout.write('Creating test workouts...')
        Workout.objects.create(name='Full Body', description='Full body workout routine', suggested_for='All')
        Workout.objects.create(name='Cardio Blast', description='Intense cardio session', suggested_for='Superheroes')

        self.stdout.write('Creating leaderboard...')
        Leaderboard.objects.create(team=marvel, points=300)
        Leaderboard.objects.create(team=dc, points=250)

        self.stdout.write('Ensuring unique index on email field in users collection...')
        db = connection.cursor().db_conn
        db.users.create_index({'email': 1}, unique=True)

        self.stdout.write(self.style.SUCCESS('Database populated with test data.'))
