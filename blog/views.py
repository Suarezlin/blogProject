from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from comments.forms import CommentForm
import markdown


def index(req):
    post_list = Post.objects.all().order_by('-created_time')
    return render(req, 'blog/index.html', context={
        'post_list': post_list
    })


def detail(req, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc'
                                  ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list
    }
    return render(req, 'blog/detail.html', context=context)


def archives(req, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(req, 'blog/index.html', context={
        'post_list': post_list
    })


def category(req, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(req, 'blog/index.html', context={
        'post_list': post_list
    })
