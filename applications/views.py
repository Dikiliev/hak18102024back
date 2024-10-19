from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import ApplicationType, Application
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

    def get_queryset(self):
        """Возвращаем только те заявления, которые принадлежат текущему пользователю."""
        user = self.request.user
        if user.is_staff:
            return Application.objects.all()  # Администраторы видят все заявления
        return Application.objects.filter(student=user)

    def create(self, request, *args, **kwargs):
        # Логика для создания заявления
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # Автоматически добавляем текущего пользователя и тип заявления
        application_type = ApplicationType.objects.get(id=self.request.data.get('application_type'))
        serializer.save(student=self.request.user, application_type=application_type)