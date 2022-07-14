from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser,IsAuthenticated,AllowAny

from utils.views import BaseRetrieveAPIView
from user.models import User
from user.serializers import UserSerializer

# Create your views here.
def index(request):
    return HttpResponse("This is user index page")


class UserInfo(BaseRetrieveAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        return User.objects.get(id=1)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['roles'] = data['roles'].split(',')
        return Response(data)