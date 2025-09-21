from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'status', 'created_at', 'updated_at', 'due_date']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_title(self, value):
        """Validate that title is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty")
        return value.strip()

    def validate_priority(self, value):
        """Validate priority choices"""
        valid_priorities = ['low', 'medium', 'high']
        if value not in valid_priorities:
            raise serializers.ValidationError(f"Priority must be one of: {valid_priorities}")
        return value

    def validate_status(self, value):
        """Validate status choices"""
        valid_statuses = ['pending', 'in_progress', 'completed']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Status must be one of: {valid_statuses}")
        return value
