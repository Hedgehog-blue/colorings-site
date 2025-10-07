from rest_framework import serializers
from .models import Author, Coloring, Pencil

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "bio"]

class ColoringSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    class Meta:
        model = Coloring
        fields = ["id", "title", "author", "theme", "pages", "price", "currency", "sku", "description"]
    def validate_price(self, v):
        if v is None or v <= 0: raise serializers.ValidationError("Price must be > 0")
        return v
    def validate_pages(self, v):
        if v < 0: raise serializers.ValidationError("Pages must be >= 0")
        return v

class PencilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pencil
        fields = ["id", "name", "brand", "hardness", "price", "currency", "sku"]
    def validate_price(self, v):
        if v is None or v <= 0: raise serializers.ValidationError("Price must be > 0")
        return v
