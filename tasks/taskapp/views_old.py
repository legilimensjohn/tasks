from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Task
from .serializers import TaskSerializer

# Create your views here.

def home(request):
    """Simple home view to test URL routing"""
    return JsonResponse({
        'message': 'Welcome to Task API!',
        'api_endpoint': '/api/',
        'admin': '/admin/'
    })

@api_view(['GET'])
def api_info(request):
    """API information endpoint"""
    return Response({
        'message': 'Task API is working!',
        'version': '1.0',
        'endpoints': {
            'GET /api/tasks/': 'List all tasks',
            'POST /api/tasks/': 'Create a new task',
            'GET /api/tasks/<id>/': 'Get specific task',
            'PUT /api/tasks/<id>/': 'Update specific task',
            'PATCH /api/tasks/<id>/': 'Partially update specific task',
            'DELETE /api/tasks/<id>/': 'Delete specific task'
        }
    })


class TaskViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling CRUD operations on Task model.
    Provides:
    - GET /api/tasks/ - List all tasks
    - POST /api/tasks/ - Create a new task
    - GET /api/tasks/{id}/ - Retrieve a specific task
    - PUT /api/tasks/{id}/ - Update a specific task
    - PATCH /api/tasks/{id}/ - Partially update a specific task
    - DELETE /api/tasks/{id}/ - Delete a specific task
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
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

@csrf_exempt
@require_http_methods(["GET", "POST"])
def task_list(request):
    """
    GET: Retrieve all tasks
    POST: Create a new task
    """
    if request.method == 'GET':
        tasks = Task.objects.all()
        tasks_data = []
        for task in tasks:
            tasks_data.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'priority': task.priority,
                'status': task.status,
                'created_at': task.created_at.isoformat(),
                'updated_at': task.updated_at.isoformat(),
                'due_date': task.due_date.isoformat() if task.due_date else None,
            })
        return JsonResponse({'tasks': tasks_data})
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            task = Task.objects.create(
                title=data.get('title'),
                description=data.get('description', ''),
                priority=data.get('priority', 'medium'),
                status=data.get('status', 'pending'),
                due_date=parse_datetime(data.get('due_date')) if data.get('due_date') else None
            )
            return JsonResponse({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'priority': task.priority,
                'status': task.status,
                'created_at': task.created_at.isoformat(),
                'updated_at': task.updated_at.isoformat(),
                'due_date': task.due_date.isoformat() if task.due_date else None,
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def task_detail(request, task_id):
    """
    GET: Retrieve a specific task
    PUT: Update a specific task
    DELETE: Delete a specific task
    """
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'GET':
        return JsonResponse({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'status': task.status,
            'created_at': task.created_at.isoformat(),
            'updated_at': task.updated_at.isoformat(),
            'due_date': task.due_date.isoformat() if task.due_date else None,
        })
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            task.title = data.get('title', task.title)
            task.description = data.get('description', task.description)
            task.priority = data.get('priority', task.priority)
            task.status = data.get('status', task.status)
            if data.get('due_date'):
                task.due_date = parse_datetime(data.get('due_date'))
            task.save()
            
            return JsonResponse({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'priority': task.priority,
                'status': task.status,
                'created_at': task.created_at.isoformat(),
                'updated_at': task.updated_at.isoformat(),
                'due_date': task.due_date.isoformat() if task.due_date else None,
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == 'DELETE':
        task.delete()
        return JsonResponse({'message': 'Task deleted successfully'}, status=200)
