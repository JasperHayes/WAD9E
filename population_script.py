import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD9E.settings')

import django
django.setup()
from GUSpeedruns.models import UserProfile, Game, Run, Comment
from django.contrib.auth.models import User
import datetime

def populate():
    user_hold = []
    game_hold = []
    run_hold = []

    users = [
        {'username': 'JamesSpeedrunner', 'password': "pword", 'email': 'jamesspeedrunner@gmail.com', 'moderator' : False},
        {'username': 'AlexiSpeedrunner', 'password': "passw", 'email': 'alexispeedrunner@gmail.com', 'moderator' : False},
        {'username': 'KatherineModerator', 'password': "passcode", 'email': 'jamesspeedrunner@gmail.com', 'moderator' : True},
    ]

    games = [
        {'name': 'Minecraft', 'date': datetime.date(2009,5,17), 'image': "game_images/Minecraft_2024_cover_art_zinWGjY.png"},
        {'name': 'Hollow Knight', 'date': datetime.date(2017,2,24), 'image': "game_images/hollowknight-1280-1529623462572_160w_W0fNkIL.webp"},
    ]

    runs = [
        {'game': 0 ,'user': 0, 'time': datetime.timedelta(hours=0,minutes=6,seconds=50,milliseconds=359), 'video': "rVs0EdiVefM",'description': "seed: -8717682453392808086"},
        {'game': 0 ,'user': 1, 'time': datetime.timedelta(hours=0,minutes=7,seconds=1,milliseconds=494), 'video': "E3t24Urba6Y",'description': "seed: 8802654848425114236"},
        {'game': 1 ,'user': 0, 'time': datetime.timedelta(hours=0,minutes=30,seconds=49,milliseconds=0), 'video': "AyqJ8xkqBMo",'description': "bad"},
        {'game': 1 ,'user': 1, 'time': datetime.timedelta(hours=0,minutes=30,seconds=53,milliseconds=0), 'video': "nQdJunydzZ8",'description': "a new era"},
    ]

    comments = [
        {'run': 0, 'user': 0, 'title': "damn", 'content': "nice time!"},
        {'run': 0, 'user': 2, 'title': "impressive", 'content': "never thought I'd see a sub-7!"},
        {'run': 3, 'user': 1, 'title': "not bad", 'content': "I just beat it :)"}
    ]

    for user in users:
        u = add_user(user['username'], user['password'], user['email'], user['moderator'])
        user_hold.append(u)
    

    for game in games:
        g = add_game(game['name'], game['date'], game['image'])
        game_hold.append(g)

    for run in runs:
        game = game_hold[run['game']]
        user = user_hold[run['user']]
        r = add_run(game, user, run['time'], run['video'], run['description'])
        run_hold.append(r)

    for comment in comments:
        run = run_hold[comment['run']]
        user = user_hold[comment['user']]
        add_comment(run, user, comment['title'], comment['content'])


def add_user(username, password, email, moderator):
    u = User.objects.get_or_create(username=username)[0]
    u.email=email
    u.is_staff = moderator
    u.set_password(password)
    u.save()
    p = UserProfile.objects.get_or_create(user=u)[0]
    p.save()
    return p
    
def add_game(name, date, image, views = 0):
    g = Game.objects.get_or_create(
        name = name,
        date_released = date,
        defaults={
            'views': views,
        })[0]
    if image:
        g.image = image
    g.save()
    return g

def add_run(game, user, time, video, description):
    r, created = Run.objects.get_or_create(
        game = game, 
        user = user,
        defaults={
            "time": time,
            "video_url_id": video,
            "description": description
        })
    
    if not created:
        r.time = time
        r.video_url_id = video
        r.description = description
        r.save()
    return r

def add_comment(run, user, title, content):
    c = Comment.objects.get_or_create(run = run, 
        title = title,
        user = user,
        defaults={
            "content": content
        })[0]
    c.save()
    return c

if __name__ == "__main__":
    print("Starting GUSpeedrun population script...")
    populate()
    print("Population complete")