from django.db import models, connection
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse

class Tag(models.Model):
    name = models.CharField(max_length=31, primary_key=True)




class Relations(models.Model):
    parent = models.ForeignKey('Branch', on_delete=models.CASCADE)
    child = models.ForeignKey('Branch', on_delete=models.CASCADE, related_name='children')

class Branch(models.Model):
    title = models.CharField(max_length=255)
    language = models.ForeignKey('Language', on_delete=models.PROTECT, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    likes = models.IntegerField(blank=True, default=0, editable=False)
    tags = models.ManyToManyField('Tag', blank=True)
    views = models.IntegerField(blank=True, default=0, editable=False)
    time_create = models.TimeField(auto_now_add=True, editable=False, blank=True)
    time_update = models.TimeField(auto_now=True, blank=True, editable=False)
    links = models.ManyToManyField('self', blank=True, symmetrical=False, through='Relations', through_fields=('parent','child' ),)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, null=True)
    pre_karma = models.IntegerField(editable=False, blank=True, null=True, db_index=True)
    karma = models.IntegerField(editable=False, blank=True, default=0)


    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('node-show-branch', kwargs={'slug': self.slug})

    @property
    def tags_indexing(self):
        """skills for indexing.
        Used in Elasticsearch indexing.
        """
        return [tag.name for tag in self.tags.all()]

    def call_my_procedure(self):
        with connection.cursor() as cursor:
            cursor.execute('call update_karma()')



class User(AbstractUser):
    liked_Branches = models.ManyToManyField('Branch', related_name='user_liked_Branches', blank=True, editable=False)
    learned_Branches = models.ManyToManyField('Branch', related_name='user_learned_Branches', blank=True,
                                              editable=False)
    wanted_to_Branches = models.ManyToManyField('Branch', related_name='user_wanted_to_learn_Branches', blank=True)
    language = models.ManyToManyField('Language', related_name='user_language', blank=True)


class Language(models.Model):
    name = models.CharField(max_length=15, primary_key=True)
