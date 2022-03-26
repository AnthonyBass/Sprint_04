from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .models import Group, Post
from .forms import PostForm

@login_required
def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, settings.POSTS_STANDARD_QTY)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)

@login_required
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.order_by('-pub_date')
    paginator = Paginator(posts, settings.POSTS_STANDARD_QTY)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)

def profile(request, username):
    user_name = User.objects.get(username=username)
    posts = Post.objects.filter(author=user_name)
    page_count = posts.count()
    paginator = Paginator(posts, settings.POSTS_STANDARD_QTY)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'user_name': user_name,
        'page_count': page_count,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)

def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    user_name = User.objects.get(username=post.author)
    b = Post.objects.filter(author=user_name)
    page_count = b.count()
    context = {
        'post': post,
        'page_count': page_count,
        'user_name': user_name,
    }
    return render(request, 'posts/post_detail.html', context) 

def post_create(request):
    error = ''
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            Post = form.save(commit=False)
            Post.author = request.user
            Post.save()
        else:
            error = 'Неверные данные'
    form = PostForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'posts/create_post.html', data)
