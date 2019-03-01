from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from django.urls import path


from apps.users.views import Registered,ObtainJSONWebToken


router = DefaultRouter()
router.register(r'Registered', Registered, base_name='Registered')  # 注册

urlpatterns = [
    path('', include(router.urls)),
    path('login/',ObtainJSONWebToken.as_view()),
    # path('GetUser/',GetUser.as_view(),name='GetUser'),
    ]
