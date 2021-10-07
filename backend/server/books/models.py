from django.db import models
from django.conf import settings

# Create your models here.

class Tag(models.Model):    
    tag_name = models.CharField(max_length=20)


class Book(models.Model):
    isbn = models.CharField(max_length=13)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    translator = models.CharField(max_length=100, null=True)
    publisher = models.CharField(max_length=100)
    publish_date = models.DateField()
    book_img = models.CharField(max_length=100)
    price = models.IntegerField()
    page = models.IntegerField(null=True)
    content = models.TextField(null=True)
    kb_score = models.FloatField(null=True)
    kb_review_cnt = models.IntegerField(null=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_books')
    read_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='BookReadUser', related_name='read_books')
    tags = models.ManyToManyField(Tag, related_name='books')
# 태그 컨텐트 리뷰카운트 스코어


class BookReadUser(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    read_at = models.DateField()

    class Meta:
        db_table = 'book_read_users'


class Category(models.Model):
    # 1 대 1 관계 -> 단수
    book = models.OneToOneField(
        Book, on_delete=models.CASCADE, related_name='category')
    category_first = models.CharField(max_length=10)
    category_second = models.CharField(max_length=10, null=True)
    category_third = models.CharField(max_length=10, null=True)
    category_fourth = models.CharField(max_length=10, null=True)
    category_fifth = models.CharField(max_length=10, null=True)


class Review(models.Model):
    # 1 대 N 관계 -> 복수
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
