from django.urls import path, include, re_path
from . import views


urlpatterns = [
    # 책 1개 조회
    path('', views.book),
    # 리뷰 개수가 100개 이상인 책 리스트
    path('list/', views.book_list),
    # 찜 등록/삭제
    path('like/', views.book_like),
    # 찜 리스트
    path('like/list/', views.like_list),
    # 읽음 등록/삭제
    path('read/', views.book_read),
    # 읽음 리스트
    path('read/list/', views.read_list),
    # 리뷰 등록/수정/삭제
    path('review/', views.review),
    # 리뷰 리스트 조회
    path('review/list/', views.review_list),
    # 추천
    path('recommend/tag/', views.recommend_tag),
    path('recommend/content/', views.recommend_content),
]
