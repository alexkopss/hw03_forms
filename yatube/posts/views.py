# from multiprocessing import context
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from .forms import PostForm
from .models import Post, Group, User


# Главная страница
def index(request):
    # Одна строка вместо тысячи слов на SQL:
    # в переменную posts будет сохранена выборка из 10 объектов модели Post,
    # отсортированных по полю по убыванию (от больших значений к меньшим)
    post_list = Post.objects.all().order_by('-pub_date')
    # Если порядок сортировки определен в классе Meta модели,
    # запрос будет выглядить так:
    # post_list = Post.objects.all()
    # Показывать по 10 записей на странице.
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # В словаре context отправляем информацию в шаблон
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


# Страница со списком мороженого
def group_posts(request, slug):
    # Функция get_object_or_404 получает по заданным критериям объект
    # из базы данных или возвращает сообщение об ошибке, если объект не найден.
    # В нашем случае в переменную group будут переданы объекты модели Group,
    # поле slug у которых соответствует значению slug в запросе
    group = get_object_or_404(Group, slug=slug)

    # Метод .filter позволяет ограничить поиск по критериям.
    # Это аналог добавления
    # условия WHERE group_id = {group_id}
    posts = Post.objects.filter(group=group).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = User.objects.get(username=username)
    post_list = Post.objects.filter(author=author)
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
    post_det = Post.objects.filter(id=post_id)
    author_posts = Post.objects.filter(id=post_id).count()
    context = {
        'post_det': post_det,
        'author_posts': author_posts,
    }
    return render(request, 'posts/post_detail.html', context)


# def post_create(request):
#     post_det = Post.objects.all
#     context = {
#         'post_det': post_det,
#     }
#     return render(request, 'posts/post_create.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=post.author)

        return render(request, 'posts/post_create.html', {'form': form})

    form = PostForm()
    return render(request, 'posts/post_create.html', {'form': form})


# @login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    is_edit = True
    if request.method == 'GET':
        form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect('posts:profile', post_id=post_id)
        else:
            form = PostForm(instance=post)
    return render(
        request,
        'posts/post_create.html',
        {'form': form, 'is_edit': is_edit, 'post_id': post_id}
    )


# @login_required()
# def post_edit(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
#     is_edit = True
#     template = 'posts/create_post.html'
#     if request.user == post.author:
#         form = PostForm(
#             request.POST or None,
#             instance=post
#         )
#         if form.is_valid():
#             form.save()
#             return redirect('post_detail', post_id=post_id)
#     context = {
#         'post_id': post_id,
#         'form': form,
#         'is_edit': is_edit
#     }
#     return render(request, template, context)