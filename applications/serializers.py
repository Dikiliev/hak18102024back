from rest_framework import serializers
from .models import Application, ApplicationType, ApplicationField, ApplicationComment
from users.models import User

class ApplicationTypeSerializer(serializers.ModelSerializer):
    fields = serializers.SerializerMethodField(method_name='get_application_fields')  # Используем метод с новым именем

    class Meta:
        model = ApplicationType
        fields = ['id', 'name', 'description', 'fields']

    def get_application_fields(self, obj):
        """Возвращаем связанные поля"""
        fields = obj.fields.all()
        return ApplicationFieldSerializer(fields, many=True).data


class ApplicationFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationField
        fields = ['id', 'name', 'field_type', 'is_required', 'template']


class ApplicationCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = ApplicationComment
        fields = ['id', 'user', 'text']


class ApplicationSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source='student.username')
    application_type = ApplicationTypeSerializer(read_only=True)
    fields = ApplicationFieldSerializer(many=True, source='application_type.fields', read_only=True)
    reviewer_comment = ApplicationCommentSerializer(read_only=True, allow_null=True)
    prorector_comment = ApplicationCommentSerializer(read_only=True, allow_null=True)
    data = serializers.JSONField()  # Поле для хранения пользовательских данных

    class Meta:
        model = Application
        fields = [
            'id', 'student', 'application_type', 'status', 'fields', 'data',
            'sent_document', 'ready_document', 'student_signature',
            'reviewer_comment', 'prorector_comment', 'submission_date', 'updated_at'
        ]

    def create(self, validated_data):
        student = self.context['request'].user
        application_type = self.context['application_type']  # Получаем тип из контекста
        data = validated_data.get('data', {})
        sent_document = validated_data.get('sent_document', None)
        student_signature = validated_data.get('student_signature', None)

        return Application.objects.create(
            student=student,
            application_type=application_type,
            data=data,
            sent_document=sent_document,
            student_signature=student_signature,
            status=Application.Status.CREATED
        )
