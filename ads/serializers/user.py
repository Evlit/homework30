from rest_framework import serializers

from ads.models import User, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = User
        exclude = ['password']


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    location = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field='name'
    )

    def is_valid(self, raise_exception=False):
        self._location = self.initial_data.pop("location")
        super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])

        for loc in self._location:
            obj, _ = Location.objects.get_or_create(name=loc)
            user.location.add(obj)

        user.save()
        return user

    class Meta:
        model = User
        fields = '__all__'


class UserUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    location = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field='name'
    )

    def is_valid(self, raise_exception=False):
        self._location = self.initial_data.pop("location")
        self._password = self.initial_data.pop("password")
        super().is_valid(raise_exception=raise_exception)

    def save(self):
        user = super().save()
        if self._password:
            user.set_password(self._password)

        for loc in self._location:
            obj, _ = Location.objects.get_or_create(name=loc)
            user.location.add(obj)

        user.save()
        return user

    class Meta:
        model = User
        fields = '__all__'


class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id"]
