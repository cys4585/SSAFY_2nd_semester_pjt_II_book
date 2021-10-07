import re
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .serializers import UserSerializer

from books.models import Book
from books.serializers import ReviewSerializer
from django.shortcuts import get_object_or_404

from .models import User

from django.conf import settings
from django.http import JsonResponse
import requests
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from json.decoder import JSONDecodeError

from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from django.contrib.auth import views as auth_views
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class CustomPasswordResetView(auth_views.PasswordResetView):
    permissions_classes = [AllowAny]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    permissions_classes = [AllowAny]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    permissions_classes = [AllowAny]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    permissions_classes = [AllowAny]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@api_view(['DELETE'])
def signout(request):
    # print(request.data)
    req_password = request.data.get('password')
    user = request.user
    if check_password(req_password, user.password):
        user.delete()
        return Response({'message': '{user.pk}번 유저 데이터 삭제완료'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'message': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)


# username/email 중복검사
@api_view(['GET'])
@permission_classes([AllowAny])
def duplicate_check(request):
    username = request.GET.get('username')
    email = request.GET.get('email')
    result = {}
    if username:
        if User.objects.filter(username=username).exists():
            result['message'] = f'{username} is exist'
            stat = status.HTTP_200_OK
        else:
            result['message'] = f'{username} is not exist'
            stat = status.HTTP_204_NO_CONTENT
    elif email:
        if User.objects.filter(email=email).exists():
            result['message'] = f'{email} is exist'
            stat = status.HTTP_200_OK
        else:
            result['mesasge'] = f'{email} is not exist'
            stat = status.HTTP_204_NO_CONTENT
    else:
        return Response({'message': 'username 혹은 email을 파라미터로 보내주세요.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(result, status=stat)

# ========================================================================================================
# ========================================================================================================
# ========================================================================================================
# 소셜 로그인 코드 흐름
# code request -> 성공시 callback으로 code 받음
# code로 access token 요청 -> 성공시 access token으로 email 값 요청
# email, access token, code를 바탕으로 회원가입/로그인 진행


BASE_URL = 'http://localhost:8000/'
KAKAO_CALLBACK_URI = BASE_URL + 'accounts/kakao/callback/'


def kakao_login(request):
    rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
    # 인가 코드 받기
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )


def kakao_callback(request):
    rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
    code = request.GET.get("code")

    redirect_uri = KAKAO_CALLBACK_URI
    """
    Access Token Request
    """
    token_req = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")
    """
    Email Request
    """
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
    profile_json = profile_request.json()
    kakao_account = profile_json.get('kakao_account')
    """
    kakao_account에서 이메일 외에
    카카오톡 프로필 이미지, 배경 이미지 url 가져올 수 있음
    print(kakao_account) 참고
    """
    # print(kakao_account)
    email = kakao_account.get('email')

    """
    Signup or Signin Request
    """
    data = {'access_token': access_token, 'code': code}

    accept = requests.post(
        f"{BASE_URL}accounts/kakao/login/finish/", data=data)
    accept_status = accept.status_code
    if accept_status != 200:
        return JsonResponse({'err_msg': 'failed to signup or signin'}, status=accept_status)
    accept_json = accept.json()
    accept_json.pop('user', None)
    return JsonResponse(accept_json)


class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI


# -----------------------------------------------

# user 수정
@api_view(['PATCH'])
def about_user(request):
    user = request.user
    # # 비밀번호 검사를 back에서 해주나??
    # if request.data.get('password2'):
    #     pwd = request.data.get('password2')
    #     user.set_password(pwd)
    #     user.save()
    # else:
    #     pwd = user.password
    if request.data.get('email'):
        email = request.data.get('email')
    else:
        email = user.email
    if request.data.get('last_name'):
        last_name = request.data.get('last_name')
    else:
        last_name = user.last_name
    if request.data.get('first_name'):
        first_name = request.data.get('first_name')
    else:
        first_name = user.first_name

    data = {
        'username': user.username,
        'email': email,
        'last_name': last_name,
        'first_name': first_name,
        'password': user.password,
    }
    serializer = UserSerializer(user, data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)


# 내 리뷰 리스트
@api_view(['GET'])
def review_list(request):
    user = request.user
    reviews = user.reviews.all()
    serializer = ReviewSerializer(reviews, many=True)
    for idx, review in enumerate(reviews):
        book = review.book
        book_title = book.title
        serializer.data[idx]['book_title'] = book_title
    return Response(serializer.data, status=status.HTTP_200_OK)
