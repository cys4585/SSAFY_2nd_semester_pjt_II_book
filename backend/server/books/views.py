from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, get_list_or_404

from rest_framework import response
from .serializers import BookSerializer, ReviewSerializer, BookReadUserSerializer
from .models import Book, BookReadUser, Review, Category, Tag
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import status
from django.http.response import JsonResponse
from . import rec_data
from . import rec_content
from django.core.paginator import Paginator
from django.db.models.query_utils import Q

from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

User = settings.AUTH_USER_MODEL


# 책 하나 정보
@api_view(['GET'])
def book(request):
    book_id = request.GET.get('book_id')
    book = get_object_or_404(Book, pk=book_id)
    serializer = BookSerializer(book)
    return Response(serializer.data)


# 리뷰 개수 TOP 12 책 리스트
@api_view(['GET', 'POST'])
def review_cnt(request):
    if request.method == 'GET':
        books = Book.objects.order_by('-kb_review_cnt')[:12]
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# # 리뷰 개수 100개 이상 책 리스트
# @api_view(['GET'])
# def books(request):
#     books = Book.objects.filter(kb_review_cnt__gte=100)
#     serializer = BookSerializer(books, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def book_list(request):
    res_data = {'book_list': None}
    books = None

    base = request.GET.get('base')
    if base == 'review_cnt':
        books = Book.objects.filter(
            kb_review_cnt__gte=int((request.GET.get('min_review_cnt'))))
    elif base == 'category':
        category_first = request.GET.get('category_first')
        category_second = request.GET.get('category_second')
        category_third = request.GET.get('category_third')
        category_fourth = request.GET.get('category_fourth')
        category_fifth = request.GET.get('category_fifth')
        book_ids = Category.objects.filter(category_first=category_first, category_second=category_second,
                                           category_third=category_third, category_fourth=category_fourth, category_fifth=category_fifth).values('book_id')
        books = Book.objects.filter(id__in=book_ids)
    elif base == 'search':
        word = request.GET.get('word')
        # 제목, 저자, 출판사, ISBN
        books = Book.objects.filter(
            Q(title__contains=word) | Q(author__contains=word) | Q(publisher__contains=word) | Q(isbn=word) | Q(content__contains=word))
    elif base == 'tag':
        tags = request.GET.get('tags').split(',')
        tags = Tag.objects.filter(tag_name__in=tags)
        for tag in tags:
            if not books:
                books = tag.books.all()
            else:
                books = books.union(tag.books.all())
    else:
        books = Book.objects.all()

    # pagination 처리
    if request.GET.get('cnt_per_page'):
        cnt_per_page = int(request.GET.get('cnt_per_page'))
        page_num = 1
        if request.GET.get('page_num'):
            page_num = int(request.GET.get('page_num'))
        paginator = Paginator(books, cnt_per_page)
        last_page = len(paginator.page_range)

        if page_num < 1 or last_page < page_num:
            return Response({'detail': f'조건: 1 <= page_num <= {last_page}'}, status=status.HTTP_400_BAD_REQUEST)
        books = paginator.get_page(page_num)
        res_data['last_page'] = last_page
    serializer = BookSerializer(books, many=True)
    res_data['book_list'] = serializer.data
    return Response(res_data, status=status.HTTP_200_OK)


# 찜
@api_view(['POST', 'DELETE'])
def book_like(request):
    book_ids = request.data.get('book_ids')
    book_id = request.data.get('book_id')

    user = request.user
    # book ids 리스트가 들어오면
    if book_ids:
        for i in range(len(book_ids)):
            print(i)
            user.like_books.add(book_ids[i])
        return JsonResponse(data={'detail': '등록 성공'})
    elif book_id:
        if request.method == 'POST':
            book = Book.objects.get(pk=book_id)
            # book.like_users.remove(request.user)
            book.like_users.add(user)
            liked = True
        elif request.method == 'DELETE':
            book = Book.objects.get(pk=book_id)
            book.like_users.remove(user)
            liked = False
        like_status = {
            'liked': liked,
            'count': book.like_users.count()
        }
        return JsonResponse(data=like_status)


# 찜 리스트
@api_view(['GET'])
def like_list(request):
    user = request.user
    books = user.like_books.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 읽음
@api_view(['POST', 'DELETE'])
def book_read(request):
    book_id = request.data.get('book_id')
    read_date = request.data.get('read_at')
    user = request.user

    book = Book.objects.get(pk=book_id)

    if request.method == 'POST':
        book_read_user = BookReadUser.objects.create(
            book=book, user=user, read_at=read_date)
        book_read_user.save()
        book.read_users.add(user)
        read = True
    elif request.method == 'DELETE':
        # Q. delete하고 다시 읽음 등록하면 book_read_users에 id가 지운거 다음부터 옴 => 원래그런가????
        book.read_users.remove(user)
        read = False
    read_status = {
        'read': read,
        'count': book.read_users.count()
    }
    return JsonResponse(data=read_status)


# 읽음 리스트
@api_view(['GET'])
def read_list(request):
    user = request.user
    books = user.read_books.all()

    book_list = BookReadUser.objects.filter(user=user)
    read_serializer = BookReadUserSerializer(book_list, many=True)

    serializer = BookSerializer(books, many=True)
    data = {
        'read_date': read_serializer.data,
        'book': serializer.data,
    }
    return Response(data, status=status.HTTP_200_OK)


# 리뷰 등록/수정/삭제
@api_view(['POST', 'PATCH', 'DELETE'])
def review(request):
    if request.method == 'POST':
        book_id = request.data.get('book_id')
        book = Book.objects.get(pk=book_id)
        # Q. 근데 읽음 한 책만 리뷰를 달 수 있나?????? 아니면 전부 다 달 수 있게????
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(book=book, user=request.user)
            print(request.user.username)
            serializer.data['user_name'] = request.user.username
            result_data = {**serializer.data, **
                           {'user_name': request.user.username}}
            print(result_data)
            return Response(result_data, status=status.HTTP_201_CREATED)
    elif request.method == 'PATCH':
        review_id = request.data.get('review_id')
        my_review = get_object_or_404(Review, pk=review_id)
        serializer = ReviewSerializer(my_review, data=request.data)
        if not request.user.reviews.filter(pk=review_id).exists():
            return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        review_id = request.data.get('review_id')
        my_review = get_object_or_404(Review, pk=review_id)
        if not request.user.reviews.filter(pk=review_id).exists():
            return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        my_review.delete()
        return Response({'id': review_id}, status=status.HTTP_204_NO_CONTENT)


# 책 1권에 대한 리뷰 리스트
@api_view(['GET'])
def review_list(request):
    book_id = request.GET.get('book_id')
    book = get_object_or_404(Book, pk=book_id)
    reviews = book.reviews.all()
    serializer = ReviewSerializer(reviews, many=True)
    for idx, review in enumerate(reviews):
        serializer.data[idx]['user_name'] = review.user.username
        serializer.data[idx]['user_id'] = serializer.data[idx].pop('user')
    return Response(serializer.data)


# 컨텐츠 기반 추천 (tag)
@api_view(['GET'])
def recommend_tag(request):
    CBF_TAGNAME_FILE = './books/fixtures/cbf_tagname.pkl'
    sim_df = rec_data.load_data(CBF_TAGNAME_FILE)

    like_books = request.user.like_books.values('id')
    user_books = [book['id'] for book in like_books]

    sim_df = sim_df.loc[user_books]
    sim_df = sim_df.transpose()

    book_id_set = set()
    for id in sim_df.columns:
        # temp = sim_df[(0.3 <= sim_df[id]) & (
        #     sim_df[id] <= 0.9)][id].index.values.tolist()
        temp = sim_df[sim_df[id] >= 0.2][id].index.values.tolist()
        book_id_set.update(temp)
    print()
    print(book_id_set)
    print()
    result_books = Book.objects.filter(
        Q(id__in=book_id_set) & Q(like_users__isnull=True))

    serializer = BookSerializer(result_books, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


# 컨텐츠 기반 추천 (content)
@api_view(['GET'])
def recommend_content(request):
    CBF_CONTENT_FILE = './books/fixtures/cbf_content.pkl'
    sim_df = rec_content.load_data(CBF_CONTENT_FILE)
    # sim_df = sim_df[0]

    like_books = request.user.like_books.values('id')
    user_book = [book['id'] for book in like_books]

    sim_df = sim_df.loc[user_book]
    sim_df = sim_df.transpose()

    book_id_set = set()
    for id in sim_df.columns:
        temp = sim_df[sim_df[id] >= 0.1][id].index.values.tolist()
        book_id_set.update(temp)

    result_books = Book.objects.filter(
        Q(id__in=book_id_set) & Q(like_users__isnull=True))

    serializer = BookSerializer(result_books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
