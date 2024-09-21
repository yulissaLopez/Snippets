from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

class SnippetSerializer(serializers.Serializer):
    # The first part of the serializer class defines the fields that get serialized/deserialized
    # y como se deben validar

    id = serializers.ImageField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length = 100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    # como se debe crear una nueva instancia del modelo
    # validated_data es un diccionario que contiene los datos que han pasado por validacion
    def create(self, validated_data):
        """
        **validated_data descompone los datos del diccionario en clave valor. Lo que significa que cada clave del diccionario se combierte en un argumento para crear el modelo
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


