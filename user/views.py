from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from utils.views import BaseRetrieveAPIView
from user.models import User
from user.serializers import UserSerializer
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView


# Create your views here.
def index(request):
    return HttpResponse("This is user index page")

# todo  add logout and refresh views, and user lists

class UserInfo(BaseRetrieveAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(pk=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['roles'] = data['roles'].split(',')
        return Response(data)

class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = 'http://10.89.228.206:28080/login/github'
    client_class = OAuth2Client