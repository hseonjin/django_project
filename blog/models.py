from configparser import MAX_INTERPOLATION_DEPTH
from django.db import models
import os
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

# Create your models here.

# tag 모델 / 다대다 관계 구현

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'

# 카테고리 기능 구현 / SlugField는 텍스트로 고유 url을 만들고 싶을 때 사용
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

    class Meta:
        verbose_name_plural = "Categories"


class Post(models.Model):
    title = models.CharField(max_length=30)

    # 본문 요약 (소제목) 생성
    hook_text = models.CharField(max_length=100, blank=True)

    # 마크다운 적용
    # content = models.TextField()
    content = MarkdownxField()

    # 사진 업로드
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)

    # 파일 업로드
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)
    # 처음 레코드가 생성될 때 현재 시각이 자동으로 저장되도록.
    # 수정할 때마다 그 시각이 지정되도록.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #  user 모델 ForeignKey로 사용
    # 작성자가 DB에서 삭제되었을 때 포스트도 같이 삭제
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 연결된 사용자가 삭제되면 포스트는 그대로 두고 작성자를 빈칸으로 두기
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


    # category 필드 추가  ForeignKey로 사용
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    # tag 필드 추가
    tags = models.ManyToManyField(Tag, blank=True)

    # 해당 포스트의 pk 값, 해당 포스트의 title 값
    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'


    # url 함수 추가 / 레코드별 url 생성 규칙 정의
    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    # 첨부파일 다운로드 파일명 나타내기
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    # 첨부파일 다운로드 확장자
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

    # 마크다운
    def get_content_markdown(self):
        return markdown(self.content)

    # 아바타 추가, 배경색 흐리게
    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/1275/d558eb306b1ea8e0/svg/{{ self.author.email }}'


# 댓글 기능 구현
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment={self.pk}'

    # 구글 아바타 설정하기
    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/1275/d558eb306b1ea8e0/svg/{{ self.author.email }}'