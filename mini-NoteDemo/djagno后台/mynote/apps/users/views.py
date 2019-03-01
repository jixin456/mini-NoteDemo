# coding=utf-8

import datetime
from mynote.sys_info import MINI_APP_ID,MINI_APP_SECRET  #导入小程序开发者的id与secret
from apps.users.models import UserProFile
from apps.users.Serializers import UserRegSerializer
from rest_framework import mixins
from rest_framework.mixins import CreateModelMixin
from rest_framework import views,viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from utils.weixin_util.weixin import WXAPPAPI
from utils.weixin_util.weixin.lib.wxcrypt import WXBizDataCrypt
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.serializers import (
    JSONWebTokenSerializer
)
from utils.permissions import IsOwnerOrReadOnly



jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

class Registered(CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):

    serializer_class = UserRegSerializer
    queryset = UserProFile.objects.all()

    # authentication_classes = (authentication.SessionAuthentication,JSONWebTokenAuthentication) #认证

    def get_permissions(self):
        if self.action =='retrieve':
            return [IsAuthenticated()]
        elif self.action =='create':
            return []
        return []

        pass

    def create(self, request, *args, **kwargs):
        api = WXAPPAPI(appid=MINI_APP_ID,app_secret=MINI_APP_SECRET)
        code = request.data['code'] #获取code
        session_info = api.exchange_code_for_session_key(code=code)
        session_key = session_info.get('session_key')
        crypt = WXBizDataCrypt(MINI_APP_ID, session_key)
        encrypted_data = request.data['username']  # 获取到encrypted_data
        iv = request.data['password']  # 获取到iv
        user_info = crypt.decrypt(encrypted_data, iv)  # 获取到用户的登陆信息
        # 获取用户的信息
        openid = user_info['openId']  # 获取openid
        avatarUrl = user_info['avatarUrl']  # 获取头像
        country = user_info['country']  # 获取国家
        province = user_info['province']  # 获取城市
        city = user_info['city']  # 获取区域
        gender = user_info['gender']  # 获取性别
        language = user_info['language']  # 获取语言
        nickName = user_info['nickName']  # 获取昵称

        # # 保存用户头像到本地
        # avatarPath = os.path.join(BASE_DIR, 'upload/UserProFilebg/avatar/')
        # avatarGet = requests.get(avatarUrl)
        # avatar_name = avatarPath + openid + '.png'
        # image = Image.open(BytesIO(avatarGet.content))
        # image.save(avatar_name)

        # 判断用户是否存在
        if UserProFile.objects.filter(openid=openid):
            this_user = UserProFile.objects.filter(openid=openid)
            this_user.nick_name = nickName  # 更新用户的微信昵称
            this_user.avatarUrl = avatarUrl  # 更新用户微信头像
            this_user.gender = str(gender)  # 更新用户的性别
            # this_user.avatar = 'avatar/' + openid + '.png'
            this_user.update()
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            # 保存用户信息
            if len(nickName) > 6:
                nickName = nickName[0:6]
            user_info_save = UserProFile()
            user_info_save.openid = openid  # 保存用户openid
            user_info_save.avatarUrl = avatarUrl  # 保存用户微信头像
            user_info_save.country = country  # 保存用户所在的国家
            user_info_save.province = province  # 保存用户所在的城市
            user_info_save.city = city  # 保存用户所在的区域
            # user_info_save.avatar = 'UserProFilebg/avatar/' + openid + '.png'
            user_info_save.gender = str(gender)  # 保存用户的性别
            user_info_save.language = language  # 保存用户当前使用的语言
            user_info_save.nick_name = nickName  # 保存用户的微信昵称
            # user_info_save.name = nickName  # 用户原始的用户名
            user_info_save.username = openid  # 保存用户的昵称
            user_info_save.password = make_password(openid)  # 保存用户的密码
            # user_info_save.zhong_jifen = 0
            user_info_save.save()

        return Response(status=status.HTTP_201_CREATED)

    def get_object(self):  # 重新来自generic view中的方法
        '''
        :return:
        '''
        return self.request.user

    def perform_create(self, serializer):
        '''
        :param serializer:
        :return:
        '''
        return serializer.save()





class READJSONWebTokenAPIView(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        try:
            username = self.request.data

            api = WXAPPAPI(appid=MINI_APP_ID, app_secret=MINI_APP_SECRET)
            code = username['code']  # 获取到code
            session_info = api.exchange_code_for_session_key(code=code)
            session_key = session_info.get('session_key')
            crypt = WXBizDataCrypt(MINI_APP_ID, session_key)
            encrypted_data = username['username']  # 获取到encrypted_data
            iv = username['password']  # 获取到iv
            user_info = crypt.decrypt(encrypted_data, iv)  # 获取到用户的登陆信息

            # 获取用户的信息
            openid = user_info['openId']  # 获取openid
            avatarUrl = user_info['avatarUrl']  # 获取到头像
            nickName = user_info['nickName']  # 获取昵称
            # 找到用户更新用户的微信昵称和头像
            this_user = UserProFile.objects.filter(openid=openid)


            if this_user:
                this_user = this_user[0]
                this_user.avatarUrl = avatarUrl
                this_user.nick_name = nickName
                # this_user.avatar = 'avatar/' + openid + '.png'
                this_user.save()

            username['username'] = openid
            username['password'] = openid
            del username['code']
        except:
            pass

        return {
            'request': self.request,
            'view': self,
        }

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ObtainJSONWebToken(READJSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.

    接收用户的用户名和密码，然后返回JWT用于认证请求
    """
    serializer_class = JSONWebTokenSerializer





# class GetUser(views.APIView):
#     '''
#     修改和获取用户的个人信息
#     '''
#     authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)  # Token验证
#     permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
#
#     def get(self, request):
#         '''
#         获取用户信息
#         :param request:
#         :return:
#         '''
#         name = self.request.user.name
#         avatar = self.request.user.avatar
#         thesignature = self.request.user.thesignature
#         background = self.request.user.background
#         gender = self.request.user.gender
#         # birthay = self.request.user.birthay
#         nickName = self.request.user.nickName
#         # mobile = self.request.user.mobile
#         if gender == '1':
#             gender = '男'
#         else:
#             gender = '女'
#         user_info = {
#             'name': name,
#             # 'avatar': IMAGES_URL + 'upload/' + str(avatar),
#             'thesignature': thesignature,
#             'gender': gender,
#             'nickName': nickName,
#             # 'mobile': mobile,
#             # 'birthay': datetime.datetime.strftime(birthay, "%Y-%m-%d"),
#             # 'background': IMAGES_URL + 'upload/' + str(background)
#         }
#         return Response(user_info, status=status.HTTP_200_OK)
#
#     def post(self, request, format=None):
#         '''
#         修改用户个人信息
#         :param request:
#         :return:
#         '''
#         try:
#             type = request.data['types']
#         except:
#             type = None
#         # if (type != None) and (image_files != None):
#         if type == 'GHTX':
#             image_files = request.data['file']
#             self.request.user.avatar = image_files
#             self.request.user.save()
#             return Response(status=status.HTTP_200_OK)
#         elif type == 'GHBJ':
#             image_files = request.data['file']
#             self.request.user.background = image_files
#             self.request.user.save()
#             return Response(status=status.HTTP_200_OK)
#         elif type == 'GHXB':
#             self.request.user.gender = request.data['new_shengri']
#             self.request.user.save()
#             return Response(status=status.HTTP_200_OK)
#         elif type == 'GHSRI':
#             self.request.user.birthay = request.data['sr']
#             self.request.user.save()
#             return Response(status=status.HTTP_200_OK)
#         elif type == 'GHNAME':
#             name_all = UserProFile.objects.filter(name=request.data['new_name'])
#             if name_all:
#                 return Response({'message': '昵称已存在'}, status=status.HTTP_202_ACCEPTED)
#             self.request.user.name = request.data['new_name']
#             self.request.user.save()
#             return Response({'message': '昵称更改成功'}, status=status.HTTP_200_OK)
#         elif type == 'GHPHONE':
#             phone_all = UserProFile.objects.filter(mobile=request.data['new_phone'])
#             if phone_all:
#                 return Response({'message': '手机号已存在'}, status=status.HTTP_202_ACCEPTED)
#             self.request.user.mobile = request.data['new_phone']
#             self.request.user.save()
#             return Response({'message': '手机号已更换'}, status=status.HTTP_200_OK)
#         elif type == 'thesignature':
#             self.request.user.thesignature = request.data['new_thesignature']
#             self.request.user.save()
#             return Response({'message': '签名已更新'}, status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
