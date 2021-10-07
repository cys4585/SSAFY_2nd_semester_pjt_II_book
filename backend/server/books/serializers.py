from django.db.models import fields
from rest_framework import serializers
from .models import Book, BookReadUser, Category, Tag, Review


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('isbn', 'title', 'author', 'translator', 'publisher', 'publish_date',
                            'book_img', 'price', 'page', 'content', 'kb_score', 'kb_review_cnt',)


# class BookListSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Book
#         fields = ('id', 'title', 'book_img', )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('book',)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'book',)


class BookReadUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookReadUser
        fields = '__all__'
