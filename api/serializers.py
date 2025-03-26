from rest_framework import serializers
from blog.models import Film

class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'