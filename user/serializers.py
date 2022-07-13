from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        # fields = ('id','author','author_id','title','content','created_time','last_modified_time','importance',
        #           'status','tags','views_count','likes_count','category','category_id')

