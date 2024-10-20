from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import ApplicationType, Application, ApplicationComment
from .serializers import ApplicationTypeSerializer, ApplicationSerializer

from rest_framework.response import Response
from rest_framework import status


class ApplicationTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ApplicationType.objects.all()
    serializer_class = ApplicationTypeSerializer
    permission_classes = []
    pagination_class = None


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        """Возвращаем только те заявления, которые принадлежат текущему пользователю."""
        user = self.request.user
        if user.is_staff:
            return Application.objects.all()  # Администраторы видят все заявления
        return Application.objects.filter(student=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        sent_document = self.request.FILES.get('sent_document')
        application_type = ApplicationType.objects.get(id=self.request.data.get('application_type'))

        files_field = dict()
        for file in self.request.FILES:
            files_field[file] = self.request.FILES.get(file)

        serializer.save(
            student=self.request.user,
            application_type=application_type,
            sent_document=sent_document,
            files_field=files_field
        )


class ProrectorApplicationListViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = Application.objects.filter(status__in=['created', 'in_progress', 'under_review'])
    queryset = Application.objects.filter()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Возвращает все заявления в статусе, которые проректор может обработать."""
        return self.queryset.order_by('-submission_date')


class ProrectorApplicationActionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def sign(self, request, pk=None):
        """Подписание заявления"""
        application = get_object_or_404(Application, pk=pk)

        # Проверка наличия подписи
        prorector_signature = request.FILES.get('prorector_signature')
        if not prorector_signature:
            return Response({"error": "Файл подписи обязателен"}, status=status.HTTP_400_BAD_REQUEST)

        # Логика для подписания заявления
        application.prorector_signature = prorector_signature
        application.status = 'completed'
        application.save()

        return Response({"message": "Заявление подписано"}, status=status.HTTP_200_OK)

    def reject(self, request, pk=None):
        """Отклонение заявления"""
        application = get_object_or_404(Application, pk=pk)


        # Получаем комментарий проректора из данных запроса
        prorector_comment_text = request.data.get('prorector_comment')
        if not prorector_comment_text:
            return Response({"error": "Комментарий обязателен для отклонения"}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем новый объект ApplicationComment с текстом комментария
        prorector_comment = ApplicationComment.objects.create(user=request.user, text=prorector_comment_text)

        # Присваиваем этот объект заявлению
        application.prorector_comment = prorector_comment
        application.status = 'rejected'
        application.save()

        return Response({"message": "Заявление отклонено"}, status=status.HTTP_200_OK)
