from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class UserProfile(models.Model):
    #user has: username, password, email, first name, last name
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #moderator if is_staff is true (base User class)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
    

class Game(models.Model):
    NAME_MAX_LENGTH = 20

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    slug_name = models.SlugField(unique=True)
    image = models.ImageField(upload_to='game_images', blank=True)
    date_released = models.DateField()
    views = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug_name = slugify(self.name)
        super(Game, self).save(*args, **kwargs)

    def __str__(self):
        return self.name



class Run(models.Model):
    TITLE_MAX_LENGTH = 100
    URL_MAX_LENGTH = 200
    DESCRIPTION_MAX_LENGTH = 200

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    title = models.CharField(max_length=TITLE_MAX_LENGTH, unique=True)
    slug_title = models.SlugField(unique=True)
    time = models.TimeField()
    video_url = models.URLField(max_length=URL_MAX_LENGTH)
    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH)

    def save(self, *args, **kwargs):
        self.title = f"{self.time} by {self.user.user.username}"
        self.slug_title = slugify(self.title)
        super(Run, self).save(*args, **kwargs)

    def __str__(self):
        return self.title



class Comment(models.Model):
    TITLE_MAX_LENGTH = 50
    CONTENT_MAX_LENGTH = 400

    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    slug_title = models.SlugField()
    content = models.CharField(max_length=CONTENT_MAX_LENGTH)

    def save(self, *args, **kwargs):
        self.slug_title = slugify(self.title)
        super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    


