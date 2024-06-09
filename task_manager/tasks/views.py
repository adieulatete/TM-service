from rest_framework import viewsets, status, permissions
from .models import Task, CustomUser
from .serializers import RegisterSerializer, TaskCreateSerializer,TaskSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action, permission_classes

from datetime import datetime, timezone


class IsCustomer(permissions.BasePermission):
    """Custom permission to check if the user is a customer."""

    def has_permission(self, request, view):
        # Checking if the current user is a customer
        return request.user.is_customer
    

class IsEmployee(permissions.BasePermission):
    """Custom permission to check if the user is an employee."""

    def has_permission(self, request, view):
        # Checking if the current user is a employee
        return request.user.is_employee


class RegisterView(APIView):
    """API endpoint for user registration."""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Handles user registration and returns tokens."""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": RegisterSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ViewSet):
    """API endpoint for listing users and getting the current user's data."""

    def list(self, request):
        queryset = CustomUser.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Retrieves the current authenticated user's data."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    

class TaskViewSet(viewsets.ViewSet):
    """API endpoint for managing tasks."""

    def list(self, request):
        """Lists all tasks related to the current user (either as customer or assignee)."""
        user = self.request.user
        queryset = Task.objects.filter(customer=user) | Task.objects.filter(assignee=user)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)
  
    @permission_classes([IsCustomer])
    @action(detail=False, methods=['post'])
    def create_task(self, request):
        """Allows a customer to create a new task."""
        # Getting the current user
        customer = request.user
        
        # Сreate an instance of the task, passing the current user as the customer
        task_data = {'customer': customer.id, **request.data} 
        # Use TaskCreateSerializer for validation
        serializer = TaskCreateSerializer(data=task_data)
        if serializer.is_valid():
            task = serializer.save(customer=customer)
            response_serializer = TaskSerializer(task)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @permission_classes([IsEmployee])
    @action(detail=False, methods=['post'])
    def take_task(self, request):
        """Allows an employee to take an available task."""
        try:
            # Receive the task by the passed identifier
            task_id = request.data.get('task_id')
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return Response({"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        # Checking if this task can be taken on
        if task.assignee:
            return Response({"message": "You are not allowed to take this task"}, status=status.HTTP_403_FORBIDDEN)

        # We assign the current user as the task executor
        task.assignee = request.user
        task.status = "IN_PROGRESS"
        task.save()

        # Returning a successful response
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_classes([IsEmployee])
    @action(detail=False, methods=['post'])
    def close_task(self, request):
        """Allows an employee to close a task with a report."""
        try:
            # Receive the task by the passed identifier
            task_id = request.data.get('task_id')
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return Response({"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        # Checking whether this task can be closed to the employee
        if task.assignee != request.user:
            return Response({"message": "You are not allowed to close this task"}, status=status.HTTP_403_FORBIDDEN)
        
        # Checking whether a task report has been written
        report = request.data.get('report')
        if report is None:
            return Response({"message": "You cannot close a task with an empty report"}, status=status.HTTP_403_FORBIDDEN)

        # Change the task status to completed
        task.status = "COMPLETED"
        task.report = report
        task.closed_at = datetime.now(tz=timezone.utc)
        task.save()

        # Returning a successful response
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_classes([IsEmployee])
    @action(detail=False, methods=['post'])
    def edit_task(self, request):
        """Allows an employee to edit a task report if the task is not completed."""
        try:
            # Receive the task by the passed identifier
            task_id = request.data.get('task_id')
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return Response({"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        # Checking whether this task can be closed to the employee
        if task.assignee != request.user | task.status == "COMPLETED":
            return Response({"message": "You are not allowed to edit this task"}, status=status.HTTP_403_FORBIDDEN)
        
        # Change the task report
        report = request.data.get('report')
        task.report = report
        task.save()

        # Returning a successful response
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    