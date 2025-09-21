from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import Task
from .serializers import TaskSerializer

@api_view(['POST'])
def simple_create_task(request):
    """Simple task creation with detailed error messages"""
    try:
        # Create task with minimal required data
        task = Task.objects.create(
            title=request.data.get('title', 'Default Task'),
            description=request.data.get('description', ''),
            priority=request.data.get('priority', 'medium'),
            status=request.data.get('status', 'pending')
        )
        
        return Response({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'status': task.status,
            'created_at': task.created_at,
            'updated_at': task.updated_at,
            'due_date': task.due_date,
            'message': 'Task created successfully!'
        }, status=201)
        
    except Exception as e:
        return Response({
            'error': str(e),
            'received_data': request.data,
            'message': 'Task creation failed'
        }, status=400)

class TaskViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling CRUD operations on Task model.
    
    Provides these endpoints:
    - GET /api/tasks/ - List all tasks
    - POST /api/tasks/ - Create a new task
    - GET /api/tasks/{id}/ - Retrieve a specific task
    - PUT /api/tasks/{id}/ - Update a specific task (full)
    - PATCH /api/tasks/{id}/ - Partially update a specific task
    - DELETE /api/tasks/{id}/ - Delete a specific task
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def list(self, request, *args, **kwargs):
        """GET /api/tasks/ - List all tasks"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """POST /api/tasks/ - Create a new task"""
        print(f"Received data: {request.data}")  # Debug print
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(f"Validation errors: {serializer.errors}")  # Debug print
        return Response({
            'errors': serializer.errors,
            'received_data': request.data,
            'message': 'Validation failed'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, *args, **kwargs):
        """GET /api/tasks/{id}/ - Get a specific task"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """PUT /api/tasks/{id}/ - Update a specific task (full update)"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        """PATCH /api/tasks/{id}/ - Partially update a specific task"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        """DELETE /api/tasks/{id}/ - Delete a specific task"""
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Task deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    def get_queryset(self):
        """
        Optionally filter tasks by status or priority
        Example: /api/tasks/?status=pending&priority=high
        """
        queryset = Task.objects.all()
        status_filter = self.request.query_params.get('status')
        priority_filter = self.request.query_params.get('priority')
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
            
        return queryset.order_by('-created_at')

def api_info(request):
    """API information endpoint"""
    return JsonResponse({
        'message': 'Task Management API',
        'version': '1.0',
        'endpoints': {
            'GET /api/tasks/': 'List all tasks',
            'POST /api/tasks/': 'Create a new task',
            'GET /api/tasks/{id}/': 'Get specific task',
            'PUT /api/tasks/{id}/': 'Update specific task (full)',
            'PATCH /api/tasks/{id}/': 'Partially update specific task',
            'DELETE /api/tasks/{id}/': 'Delete specific task'
        },
        'filters': {
            'status': 'pending, in_progress, completed',
            'priority': 'low, medium, high'
        }
    })
