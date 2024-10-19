from django.core.validators import FileExtensionValidator
from django.db import models
from users.models import User


class ApplicationField(models.Model):
    FIELD_TYPES = [
        ('text', 'Текстовое поле'),
        ('image', 'Изображение'),
        ('document', 'Документ'),
        ('signature', 'Подпись'),
    ]

    name = models.CharField(max_length=255)
    field_type = models.CharField(max_length=10, choices=FIELD_TYPES)
    is_required = models.BooleanField(default=True)

    example = models.TextField(blank=True, null=True)
    template = models.FileField(
        upload_to='applications/templates/',
        blank=True, null=True,
        validators=[FileExtensionValidator(['pdf', 'docx', 'doc'])]
    )

    def __str__(self):
        return f'{self.name} ({self.field_type})'

class ApplicationType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    fields = models.ManyToManyField(ApplicationField, related_name='application_types')  # Связь с полями

    def __str__(self):
        return self.name

class ApplicationComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()


class Document(models.Model):
    name = models.CharField(max_length=255)
    value = models.FileField(upload_to='documents/', validators=[FileExtensionValidator(['pdf', 'docx', 'doc'])])

class Application(models.Model):
    class Status(models.TextChoices):
        CREATED = 'created', 'Создано'
        UNDER_REVIEW = 'under_review', 'Проверяется'
        IN_PROGRESS = 'in_progress', 'В процессе'
        COMPLETED = 'completed', 'Готово'

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    application_type = models.ForeignKey(ApplicationType, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CREATED
    )

    sent_document = models.FileField(
        upload_to='applications/send_docs/',
        blank=True, null=True,
        validators=[FileExtensionValidator(['pdf', 'docx', 'doc'])]
    )

    ready_document = models.FileField(
        upload_to='applications/ready_docs/',
        blank=True, null=True,
        validators=[FileExtensionValidator(['pdf'])]
    )

    student_signature = models.FileField(
        upload_to='applications/signatures/',
        blank=True, null=True,
        validators=[FileExtensionValidator(['jpg', 'png'])]
    )

    reviewer_comment = models.ForeignKey(ApplicationComment, related_name='reviewer_comments', on_delete=models.SET_NULL, blank=True, null=True)
    prorector_comment = models.ForeignKey(ApplicationComment, related_name='prorector_comments', on_delete=models.SET_NULL, blank=True, null=True)

    submission_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    fields_data = models.JSONField(default=dict)

    def __str__(self):
        return f'{self.application_type.name} - {self.student.username}'

    def get_required_fields(self):
        """Возвращает список обязательных полей для текущего типа заявления"""
        return self.application_type.fields.filter(is_required=True)
