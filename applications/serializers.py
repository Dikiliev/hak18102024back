from rest_framework import serializers
from .models import ApplicationType, Application, ApplicationComment
from users.models import User


# Сериализатор для типа заявления
class ApplicationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationType
        fields = ['id', 'name', 'description']


# Сериализатор для комментариев
class ApplicationCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Выводим имя пользователя, оставившего комментарий

    class Meta:
        model = ApplicationComment
        fields = ['id', 'user', 'text']


# Сериализатор для пользователя
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# Сериализатор для заявления
class ApplicationSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)  # Сериализуем студента
    application_type = ApplicationTypeSerializer(read_only=True)  # Сериализуем тип заявления
    reviewer_comment = ApplicationCommentSerializer(read_only=True, allow_null=True)  # Комментарии проверяющего
    prorector_comment = ApplicationCommentSerializer(read_only=True, allow_null=True)  # Комментарии проректора

    class Meta:
        model = Application
        fields = [
            'id',
            'student',
            'application_type',
            'status',
            'sent_document',
            'ready_document',
            'student_signature',
            'reviewer_comment',
            'prorector_comment',
            'submission_date',
            'updated_at'
        ]

    # Метод для обработки создания заявления с загружаемыми файлами
    def create(self, validated_data):
        request = self.context.get('request')
        student = request.user  # Устанавливаем текущего пользователя как студента
        application_type = validated_data.get('application_type')
        sent_document = validated_data.get('sent_document')
        student_signature = validated_data.get('student_signature')

        # Создание нового заявления
        application = Application.objects.create(
            student=student,
            application_type=application_type,
            sent_document=sent_document,
            student_signature=student_signature,
            status=Application.Status.CREATED
        )
        return application
