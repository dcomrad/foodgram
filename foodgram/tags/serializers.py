from rest_framework import serializers

from tags.models import Tags


class TagsSerializer(serializers.ModelSerializer):
    color = serializers.RegexField('^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')

    class Meta:
        model = Tags
        fields = ['id', 'name', 'color', 'slug']
