from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time

# Create your models here.

def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))

class Post(models.Model):
    title = models.CharField('Наименование', max_length=200, db_index=True)
    slug = models.SlugField('Слаг', max_length=150, unique=True)
    body = models.TextField('Текст', blank=True, db_index=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    date_pub = models.DateTimeField('Время публикации', auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug':self.slug})
    
    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug':self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug':self.slug})

    def __str__(self):
        return f'{self.title}'
    
    def save(self, *args, **kwargs):
        print(self.slug)
        if not self.id and not self.slug:
                self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)
    class Meta:
        ordering=['-date_pub']


class Tag(models.Model):
    title = models.CharField('Наименование', max_length=50)
    slug = models.SlugField('Слаг', max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug':self.slug})
    
    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug':self.slug})
    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug':self.slug})

    def __str__(self):
        return f'{self.title}'
    class Meta:
        ordering=['title']