from django.shortcuts import render
from rest_framework import views
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from utils.permissions import IsOwnerOrReadOnly
from apps.note.models import NoteModel
from note.serializers import NoteSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import views,viewsets

# Create your views here.

class UploadTextView(views.APIView):
    authentication_classes = (authentication.SessionAuthentication,JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)

    def post(self,request):
        user = self.request.user
        content = request.data['content']

        note = NoteModel()
        note.user = user
        note.content = content
        note.save()
        return Response({'id':note.id},status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)

class GetTextView(mixins.ListModelMixin,viewsets.GenericViewSet):

    authentication_classes = (authentication.SessionAuthentication,JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)

    def get_queryset(self):
        query = NoteModel.objects.filter(user=self.request.user)
        return query
    serializer_class = NoteSerializers