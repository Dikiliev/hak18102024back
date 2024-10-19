from rest_framework import serializers
from .models import Application, ApplicationType, ApplicationField, ApplicationComment
from django.core.files.storage import default_storage


class ApplicationFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationField
        fields = ['id', 'name', 'field_type', 'is_required', 'template', 'example']


class ApplicationTypeSerializer(serializers.ModelSerializer):
    fields = ApplicationFieldSerializer(many=True)  # Сериализуем связанные поля

    class Meta:
        model = ApplicationType
        fields = ['id', 'name', 'description', 'fields']


class ApplicationTypeLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationType
        fields = ['id', 'name']


class ApplicationSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source='student.username')
    application_type = ApplicationTypeLiteSerializer(read_only=True)
    fields_data = serializers.JSONField()  # Поле для хранения произвольных данных пользователя

    sent_document = serializers.FileField(required=False, allow_null=True)
    ready_document = serializers.FileField(required=False, allow_null=True)
    student_signature = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Application
        fields = [
            'id', 'student', 'application_type', 'status', 'fields_data',
            'sent_document', 'ready_document', 'student_signature',
            'reviewer_comment', 'prorector_comment',
            'submission_date', 'updated_at'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        application_type = validated_data.get('application_type')
        fields_data = validated_data.get('fields_data', {})

        # Сохраняем заявление
        application = Application.objects.create(
            student=user,
            application_type=application_type,
            fields_data=fields_data,
            sent_document=validated_data.get('sent_document'),
            student_signature=validated_data.get('student_signature'),
            status=Application.Status.CREATED
        )

        # Сохраняем загруженные файлы и добавляем их ссылки в fields_data
        files = self.context['request'].FILES
        file_links = {}

        for field_name, file in files.items():
            file_path = default_storage.save(f'uploads/{file.name}', file)  # Сохраняем файл
            file_url = default_storage.url(file_path)  # Получаем URL сохраненного файла
            file_links[field_name] = file_url  # Добавляем ссылку в словарь

        # Обновляем fields_data с ссылками на файлы
        application.fields_data.update(file_links)
        application.save()

        return application

