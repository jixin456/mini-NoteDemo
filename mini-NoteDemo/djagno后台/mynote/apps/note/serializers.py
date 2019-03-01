from rest_framework import serializers

from apps.note.models import NoteModel



class NoteSerializers(serializers.ModelSerializer):

    class Meta:
        model = NoteModel
        fields = '__all__'
