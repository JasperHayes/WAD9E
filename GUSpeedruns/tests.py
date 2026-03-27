from datetime import date, timedelta
from unittest.mock import patch

from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.test import TestCase
from django.urls import reverse

from GUSpeedruns.models import UserProfile, Game, Run, Comment


class TestDataMixin:
    def create_user_with_profile(
        self,
        username='testuser',
        password='testpass123',
        email='test@example.com',
        is_staff=False,
        is_active=True,
    ):
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )
        user.is_staff = is_staff
        user.is_active = is_active
        user.save()

        profile = UserProfile.objects.create(user=user)
        return user, profile

    def create_game(self, name='Minecraft', views=0, release_date=None):
        if release_date is None:
            release_date = date(2011, 11, 18)

        return Game.objects.create(
            name=name,
            date_released=release_date,
            views=views,
        )

    def create_run(self, game, profile, seconds=10, video_url_id='abc123', description='Test run'):
        run = Run(
            game=game,
            user=profile,
            title='temporary',
            slug_title='temporary',
            time=timedelta(seconds=seconds),
            video_url_id=video_url_id,
            description=description,
        )
        run.save()
        return run

    def create_comment(self, run, profile, title='Nice run', content='Great job'):
        comment = Comment.objects.create(
            run=run,
            user=profile,
            title=title,
            content=content,
        )
        return comment


# model tests for slug and title.
class ModelTests(TestDataMixin, TestCase):
    def test_userprofile_save_generates_slug(self):
        user, profile = self.create_user_with_profile(username='John Smith')
        profile.refresh_from_db()

        self.assertEqual(profile.slug_name, 'john-smith')
        self.assertEqual(str(profile), 'John Smith')

    def test_game_save_generates_slug(self):
        game = self.create_game(name='Hollow Knight')

        self.assertEqual(game.slug_name, 'hollow-knight')
        self.assertEqual(str(game), 'Hollow Knight')

    def test_run_save_generates_title_and_slug(self):
        _, profile = self.create_user_with_profile(username='runner1')
        game = self.create_game(name='Portal')
        run = self.create_run(game=game, profile=profile, seconds=65)

        expected_title = f"{timedelta(seconds=65)} by runner1"
        self.assertEqual(run.title, expected_title)
        self.assertEqual(run.slug_title, slugify(expected_title))

    def test_comment_save_generates_slug(self):
        _, profile = self.create_user_with_profile(username='commenter')
        game = self.create_game(name='Celeste')
        run = self.create_run(game=game, profile=profile, seconds=90)
        comment = self.create_comment(run=run, profile=profile, title='Very Fast Run')

        self.assertEqual(comment.slug_title, 'very-fast-run')
        self.assertEqual(str(comment), 'Very Fast Run')