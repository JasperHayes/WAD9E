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

