from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
#taggit
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset()\
            .filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published','Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date = 'publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default='draft')
    objects = models.Manager() # the default manager
    published = PublishedManager() # our custom manager
    tags = TaggableManager() #3rd party tag manager

    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[self.publish.year,self.publish.month,self.publish.day,self.slug])
    
#comment system 1:Create Model, 2:Process data(Control) 3:Template(View)
#after creation, must makemigrations appname and migrate to update the database
class Comment(models.Model):
    #many to one relationships to Post, get 2 useful stuff: comment.post and post.comments.all()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    #saved the date when created
    created = models.DateTimeField(auto_now_add=True)
    #update the date when saved
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering =('created',)
    
    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)

