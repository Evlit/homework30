from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from ads.models import User, Ad, Category, Selection


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'


class AdListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    author = serializers.StringRelatedField()

    class Meta:
        model = Ad
        fields = ['id', 'name', 'author', 'price', 'description', 'is_published', 'image', 'category']


class AdCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    category = serializers.StringRelatedField()
    author = serializers.StringRelatedField()

    def is_valid(self, raise_exception=False):
        self._author = self.initial_data.pop("author")
        self._category = self.initial_data.pop("category")
        super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        author = get_object_or_404(User, username=self._author)
        category = get_object_or_404(Category, name=self._category)
        ad = Ad.objects.create(
                        name=validated_data["name"],
                        author=author,
                        price=validated_data["price"],
                        description=validated_data["description"],
                        is_published=validated_data["is_published"],
                        category=category
                    )
        ad.save()
        return ad

    class Meta:
        model = Ad
        fields = '__all__'


class AdUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    category = serializers.StringRelatedField()
    author = serializers.StringRelatedField()

    def is_valid(self, raise_exception=False):
        super().is_valid(raise_exception=raise_exception)

    def save(self):
        ad = super().save()
        ad.save()
        return ad

    class Meta:
        model = Ad
        fields = '__all__'


class AdDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ["id"]
