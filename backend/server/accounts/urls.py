
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', include('dj_rest_auth.registration.urls')),
    path('signout/', views.signout),
    path('duplicate_check/', views.duplicate_check),
    path('kakao/login/', views.kakao_login),
    path('kakao/callback/', views.kakao_callback),
    path('kakao/login/finish/', views.KakaoLogin.as_view()),
    # password reset link 발송할 수 있는 화면
    path('password_reset/', views.CustomPasswordResetView.as_view(),
         name='password_reset'),
    # password_reset link 발송 화면에서 Reset my password 버튼 누르면 나오는 화면
    path('password_reset_done/', views.CustomPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    # 사용자에게 발송되는 링크 형식(이메일에서 들어갈 수 있는 링크)
    # 비밀번호 변경 후 다시 접속하면, invalid
    path('password_reset_confirm/<uidb64>/<token>/',
         views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # change my password 를 누른 후 화면 (새로운 비밀번호 변경)
    path('password_reset_complete/', views.CustomPasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
    # user 수정
    path('about-user/', views.about_user),
    # 내 리뷰 리스트
    path('review/list/', views.review_list),
]
