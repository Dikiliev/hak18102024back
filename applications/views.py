from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Application, ApplicationType
from .serializers import ApplicationSerializer, ApplicationTypeSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class ApplicationTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ApplicationType.objects.all()
    serializer_class = ApplicationTypeSerializer
    permission_classes = []
    pagination_class = None
