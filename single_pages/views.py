from django.shortcuts import render
from blog.models import Post

# Create your views here.


def landing(request):
    # 대문페이지에 최근포스트 3개만 보여주기
    recent_posts = Post.objects.order_by('-pk')[:3]
    return render(request, 'single_pages/landing.html', {'recent_posts': recent_posts})

# def about_me(request):
#     return render (request, 'single_pages/about_me.html')
