from rest_framework.routers import DefaultRouter
from django.urls import path
from apps.note.views import UploadTextView,GetTextView
from django.conf.urls import include

router = DefaultRouter()

# router.register('upnote',UploadTextView,base_name='UploadTextView')

urlpatterns = [
    # path('',include(router.urls)),
    path('upnote/',UploadTextView.as_view()),
    path('getnote/',GetTextView.as_view({'get': 'list'})),
]