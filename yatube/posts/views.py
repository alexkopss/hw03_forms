from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from .forms import PostForm
from .models import Post, Group, User


def index(request):
    """Главная страница"""
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Страница со списком групп"""
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    posts_number = post_list.count()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'post_list': post_list,
        'posts_number': posts_number,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    author_posts = post.author.posts.count()
    context = {
        'post': post,
        'author_posts': author_posts,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """View функция страницы создания записи."""
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()
        return redirect('posts:profile', username=post.author)
    context = {
        'form': form,
    }
    return render(request, 'posts/post_create.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    is_edit = True
    form = PostForm(request.POST, instance=post)
    if post.author == request.user:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    else:
        form = PostForm(instance=post)
    return render(
        request,
        'posts/post_create.html',
        {'form': form, 'is_edit': is_edit, 'post_id': post_id}
    )
