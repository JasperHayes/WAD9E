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


# homepage: search bar and trending games page.
class HomepageViewTests(TestDataMixin, TestCase):
    def test_homepage_uses_pagination_nine_per_page(self):
        for i in range(10):
            self.create_game(
                name=f'Game{i}',
                views=i,
                release_date=date(2020, 1, min(i + 1, 28)),
            )

        response = self.client.get(reverse('GUSpeedruns:homepage'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['games']), 9)
        self.assertEqual(response.context['page_obj'].paginator.num_pages, 2)
        self.assertEqual(response.context['page_title'], 'Trending Games')

    def test_homepage_search_filters_games_by_name(self):
        minecraft = self.create_game(name='Minecraft')
        self.create_game(name='Hollow Knight')
        self.create_game(name='Portal')

        response = self.client.get(reverse('GUSpeedruns:homepage'), {'q': 'craft'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_title'], 'Search Results')
        self.assertEqual(response.context['query'], 'craft')
        self.assertEqual(list(response.context['games']), [minecraft])

    def test_show_game_increments_views_only_once_per_cookie(self):
        game = self.create_game(name='Terraria', views=0)
        url = reverse('GUSpeedruns:show_game', kwargs={'game_name_slug': game.slug_name})

        first_response = self.client.get(url)
        game.refresh_from_db()

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(game.views, 1)
        self.assertIn(f'viewed_game_{game.slug_name}', first_response.cookies)

        second_response = self.client.get(url)
        game.refresh_from_db()

        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(game.views, 1)


# register/login/my account
class AuthAndAccountViewTests(TestDataMixin, TestCase):
    def test_register_creates_user_and_profile(self):
        response = self.client.post(
            reverse('GUSpeedruns:register'),
            {
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password': 'safePassword123',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['registered'])
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(UserProfile.objects.filter(user__username='newuser').exists())

        created_user = User.objects.get(username='newuser')
        self.assertTrue(created_user.check_password('safePassword123'))

    def test_user_login_with_valid_credentials_redirects_homepage(self):
        user, _ = self.create_user_with_profile(username='loginuser', password='loginpass123')

        response = self.client.post(
            reverse('GUSpeedruns:login'),
            {
                'username': 'loginuser',
                'password': 'loginpass123',
            },
        )

        self.assertRedirects(response, reverse('GUSpeedruns:homepage'))
        self.assertEqual(int(self.client.session['_auth_user_id']), user.id)

    def test_user_login_with_invalid_credentials_sets_invalid_flag(self):
        self.create_user_with_profile(username='loginuser', password='rightpass123')

        response = self.client.post(
            reverse('GUSpeedruns:login'),
            {
                'username': 'loginuser',
                'password': 'wrongpass',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['invalid'])
        self.assertFalse(response.context['disabled'])

    def test_my_account_requires_login(self):
        response = self.client.get(reverse('GUSpeedruns:my_account'))

        self.assertEqual(response.status_code, 302)

    def test_my_account_shows_profile_runs_and_comments(self):
        user, profile = self.create_user_with_profile(username='accountuser', password='accountpass123')
        game = self.create_game(name='Cuphead')
        run = self.create_run(game=game, profile=profile, seconds=77)
        comment = self.create_comment(run=run, profile=profile)

        self.client.force_login(user)
        response = self.client.get(reverse('GUSpeedruns:my_account'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['profile_user'], profile)
        self.assertIn(run, response.context['runs'])
        self.assertIn(comment, response.context['comments'])


# moderator: upload_game/delete run
class StaffOnlyViewTests(TestDataMixin, TestCase):
    def test_upload_game_rejects_non_staff_user(self):
        user, _ = self.create_user_with_profile(username='normaluser', password='normalpass123')
        self.client.force_login(user)

        response = self.client.get(reverse('GUSpeedruns:upload_game'))

        self.assertEqual(response.status_code, 302)

    def test_upload_game_allows_staff_user_to_create_game(self):
        staff_user, _ = self.create_user_with_profile(
            username='staffuser',
            password='staffpass123',
            is_staff=True,
        )
        self.client.force_login(staff_user)

        response = self.client.post(
            reverse('GUSpeedruns:upload_game'),
            {
                'name': 'Dead Cells',
                'date_released': '2018-08-07',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Game.objects.filter(name='Dead Cells').exists())

    def test_delete_run_requires_staff_to_delete(self):
        normal_user, normal_profile = self.create_user_with_profile(username='normaluser', password='normalpass123')
        staff_user, _ = self.create_user_with_profile(
            username='staffuser',
            password='staffpass123',
            is_staff=True,
        )
        game = self.create_game(name='Super Meat Boy')
        run = self.create_run(game=game, profile=normal_profile, seconds=55)

        self.client.force_login(normal_user)
        response = self.client.post(
            reverse(
                'GUSpeedruns:delete_run',
                kwargs={
                    'game_name_slug': game.slug_name,
                    'run_name_slug': run.slug_title,
                },
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Run.objects.filter(id=run.id).exists())

        self.client.force_login(staff_user)
        response = self.client.post(
            reverse(
                'GUSpeedruns:delete_run',
                kwargs={
                    'game_name_slug': game.slug_name,
                    'run_name_slug': run.slug_title,
                },
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Run.objects.filter(id=run.id).exists())