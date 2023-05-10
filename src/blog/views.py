from django.shortcuts import render
from .models import *
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
# Create your views here.

def homepage(request):
    blog_object = Blog.objects.all()
    temp_name = 'homepage/home.html'
    context = {'posts':blog_object}
    return render(request, temp_name,context)

def blogpage(request):
    all_posts = Blog.objects.filter(status = 2)
    per_page = 2
    paginator = Paginator(all_posts, per_page)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    temp_name = 'blogs/blog.html'
    context = {'posts':page_object}
    return render(request, temp_name, context)

def singlepage(request, slug):
    post = get_object_or_404(Blog, slug = slug)
    temp_name = 'blogs/single.html'
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, temp_name, {'single_post':post,
               'comments': comments,
               'new_comment': new_comment,
               'comment_form': comment_form})

