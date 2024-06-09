from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import CustomUser, Task


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    is_customer = serializers.BooleanField(required=False)
    is_employee = serializers.BooleanField(required=True)
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        """Meta class for RegisterSerializer."""
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone', 'is_customer', 'is_employee']

    def create(self, validated_data):
        """Create a new user with the validated data."""
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser model."""
    class Meta:
        """Meta class for UserSerializer."""
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone', 'is_customer', 'is_employee']


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model."""
    customer = serializers.SerializerMethodField()
    assignee = serializers.SerializerMethodField()

    def get_customer(self, obj):
        """Get the username of the customer."""
        return obj.customer.username if obj.customer else None

    def get_assignee(self, obj):
        """Get the username of the assignee."""
        return obj.assignee.username if obj.assignee else None

    class Meta:
        """Meta class for TaskSerializer."""
        model = Task
        fields = '__all__'
