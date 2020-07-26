from django.db import models
from django.urls import reverse
import uuid
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.conf import settings

# Create your models here.

def image_path(_,filename):
    extension = filename.split('.')[-1]
    unique_id = uuid.uuid4().hex
    new_filname = unique_id+'.'+extension
    return 'post/'+new_filname

class Blogs(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to=image_path,null=True,blank=True)
    slug = models.SlugField(max_length=200,editable=True,null=True,blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='blogs',default=1)
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # count = models.IntergerField(default=0)

    class Meta :
        ordering = ('-created',)

    def save(self,*args,**kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super(Blogs,self).save(*args,**kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogposts:user_post_list', kwargs={
            'author': self.author.username, 'author_id': self.author.id})

