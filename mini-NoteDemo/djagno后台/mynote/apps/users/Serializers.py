from rest_framework import serializers

from apps.users.models import UserProFile
#Serializer 的主要工作是将 Python 数据结构序列化为其它格式（XML／JSON 等等）
class UserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProFile
        fields = ('nickName','avatarUrl','gender','password')