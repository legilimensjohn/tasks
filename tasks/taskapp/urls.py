from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import views

@api_view(['POST'])
def debug_create_task(request):
    """Debug endpoint to see what data is being received"""
    return Response({
        'received_data': request.data,
        'content_type': request.content_type,
        'method': request.method,
        'message': 'Debug endpoint working - data received successfully'
    })

app_name = 'taskapp'

# Create router for DRF ViewSet
router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet)

urlpatterns = [
    path('debug/', debug_create_task, name='debug'),  # Debug endpoint
    path('simple/', views.simple_create_task, name='simple-create'),  # Simple create
    path('', include(router.urls)),  # This creates /api/tasks/ endpoint
]
