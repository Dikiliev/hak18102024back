from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Application, ApplicationType
from .serializers import ApplicationSerializer, ApplicationTypeSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print(self.request)
        application_type = ApplicationType.objects.get(id=self.request.data.get('application_type'))
        serializer.save(student=self.request.user, application_type=application_type)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # Администратор видит все заявления
            return Application.objects.all()
        return Application.objects.filter(student=user)  # Обычные пользователи видят только свои заявления

class ApplicationTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ApplicationType.objects.all()
    serializer_class = ApplicationTypeSerializer
    permission_classes = []
    pagination_class = None
