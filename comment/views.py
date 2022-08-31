from rest_framework.response import Response
from rest_framework import status


from utils.views import BaseCreateAPIView

from article.models import Article
from comment.models import Comment
from comment.serializers import CommentSerializer

# Create your views here.
class CreateComment(BaseCreateAPIView):
    model = Comment
    serializer_class = CommentSerializer
    # permission_classes = [IsAdminUser]


    def create(self, request, *args, **kwargs):
        # print('create, get serializer -->')
        # print("request data is:{}".format(request.data))
        data = request.data
        print(data)
        article_id = data['article']
        article = Article.objects.get(id=article_id)

        serializer = self.get_serializer(data=request.data)
        # print('get serializer--> done')
        # print('begin to call serializer is_valid function')
        serializer.is_valid(raise_exception=True)
        # print('serializer.errors:{}'.format(serializer.errors))
        # print('before create-->')
        self.perform_create(serializer)
        # print('creat done')
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
