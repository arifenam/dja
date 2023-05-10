from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Category (models.Model):
    title = models.CharField (max_length=200)
    slug = models.SlugField(max_length= 70, unique= True, null= True, blank = True)

    def __str__(self):
         return self.title

    def save(self, *args, **kwargs ):
        if not self.pk:
            if not self.slug:
                self.slug = slugify(self.title)
            while Category.objects.filter(slug = self.slug).exists():
                self.slug = f'{slugify(self.title)}-{get_random_string(4)}'
            super().save(*args, **kwargs)



class Blog (models.Model):
    title = models.CharField (max_length=200)
    meta_title = models.CharField (max_length=200,null= True, blank = True)
    meta_des = models.TextField(null= True, blank = True)
    content = RichTextUploadingField(blank=True, null =True)
    slug = models.SlugField(max_length= 70, unique= True, null= True, blank = True)
    featured_img = models.ImageField(upload_to='blogs_media/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    Status = [('1','Draft'),
              ('2','Published'),
              ('3','Pending'),              
              ]
    status = models.CharField(choices=Status, default='Draft', max_length=15)
    categories = models.ForeignKey(Category, verbose_name=("all categories"), on_delete=models.CASCADE,null=True, blank=True, default=None)
    
    def __str__(self):
         return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            # This is a new object, generate a new slug
            if not self.slug:
                self.slug = slugify(self.title)
            while Blog.objects.filter(slug=self.slug).exists():
                self.slug = f'{slugify(self.title)}-{get_random_string(4)}'
        else:
            # update the slug if the title has changed
            old_post = Blog.objects.get(pk=self.pk)
            if old_post.title != self.title:
                self.slug = slugify(self.title)
                while Blog.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                    self.slug = f'{slugify(self.title)}-{get_random_string(4)}'
            
        if not self.categories:
            uncategorized = Category.objects.get_or_create(title='uncategorized')[0]
            self.categories = uncategorized

        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)



