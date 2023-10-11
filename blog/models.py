from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here.


class Auther(models.Model):
    auther = models.ForeignKey(User, on_delete=models.CASCADE)
    name= models.CharField( max_length=100)
    photo = models.ImageField(upload_to='media/authors/%Y/%m/%d/', max_length=255, blank=True, null=True)
    descreption = models.TextField( null=True, blank=True)

    def __str__(self):
        return self.name



class Category(models.Model):
   name = models.CharField( max_length=50, unique=True, blank=False)

   def __str__(self):
       return self.name


class Post(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField()
    image = models.ImageField(upload_to='media/blog/',blank=True ,default='static/images/team/team-img-03.jpg')
    date = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=300, blank=True, null=True)
    active = models.BooleanField(default=True)
    auther = models.ForeignKey(Auther,
                               on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='posts')
    tags = TaggableManager()
    
    def save(self, *args, **kwargs):
        if not self.slug :
            self.slug = slugify(self.title)
        super(Post,self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={'slug': self.slug})
   
   
class Comment(models.Model):
    message = models.TextField(max_length=7000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    created_by =models.ForeignKey(User,
                              on_delete=models.PROTECT)
    
    class Meta:
        ordering = ['created_at']
        
    def __str__(self):
        return self.message
    
    
