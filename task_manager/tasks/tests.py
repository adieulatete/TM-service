from django.test import TestCase
from .models import CustomUser, Task


class CustomUserModelTest(TestCase):
    """Test case for the CustomUser model."""
    
    def setUp(self):
        """Set up a test user."""
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='password123',
            phone='1234567890',
            is_customer=True,
            is_employee=False
        )

    def test_user_creation(self):
        """Test the creation of a user."""
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('password123'))
        self.assertEqual(self.user.phone, '1234567890')
        self.assertTrue(self.user.is_customer)
        self.assertFalse(self.user.is_employee)

    def test_user_string_representation(self):
        """Test the string representation of the user."""
        self.assertEqual(str(self.user), 'testuser')


class TaskModelTest(TestCase):
    """Test case for the Task model."""

    def setUp(self):
        """Set up test users and a test task."""
        self.customer = CustomUser.objects.create_user(
            username='customer',
            password='password123',
            phone='0987654321',
            is_customer=True,
            is_employee=False
        )
        
        self.employee = CustomUser.objects.create_user(
            username='employee',
            password='password123',
            phone='1234509876',
            is_customer=False,
            is_employee=True
        )
        
        self.task = Task.objects.create(
            title='Test Task',
            customer=self.customer,
            assignee=self.employee,
            status='IN_PROGRESS',
            report='This is a test report.'
        )

    def test_task_creation(self):
        """Test the creation of a task."""
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.customer, self.customer)
        self.assertEqual(self.task.assignee, self.employee)
        self.assertEqual(self.task.status, 'IN_PROGRESS')
        self.assertEqual(self.task.report, 'This is a test report.')
        self.assertIsNotNone(self.task.created_at)
        self.assertIsNotNone(self.task.updated_at)
        self.assertIsNone(self.task.closed_at)

    def test_task_status_choices(self):
        """Test the status choices of a task."""
        self.task.status = 'COMPLETED'
        self.task.save()
        self.assertEqual(self.task.status, 'COMPLETED')
        self.assertIn(self.task.status, dict(Task.STATUS_CHOICES))

    def test_task_string_representation(self):
        """Test the string representation of the task."""
        self.assertEqual(str(self.task), 'Test Task')
