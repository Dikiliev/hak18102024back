from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from users.models import User
from utils import send_status_change_email
from .models import ApplicationType, Application, ApplicationComment
from .serializers import ApplicationTypeSerializer, ApplicationSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


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
        if user.role == User.Roles.STUDENT:
            return Application.objects.filter(student=user).order_by('-submission_date')

        return Application.objects.all().order_by('-submission_date')


    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def change_status(self, request, pk=None):
        application = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(Application.Status.choices).keys():
            return Response({'error': 'Недопустимый статус.'}, status=status.HTTP_400_BAD_REQUEST)

        application.status = new_status
        application.save()

        send_status_change_email(application.student.email, application, new_status)

        serializer = self.get_serializer(application)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated],
            parser_classes=[MultiPartParser, FormParser])
    def accept(self, request, pk=None):
        application = self.get_object()

        user = request.user

        application.status = Application.Status.IN_PROGRESS
        application.save()

        send_status_change_email(application.student.email, application, application.get_status_display())

        serializer = self.get_serializer(application)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated],
            parser_classes=[MultiPartParser, FormParser, JSONParser])
    def reject(self, request, pk=None):
        application = self.get_object()
        user = request.user

        comment_text = request.data.get('comment')
        if not comment_text:
            return Response({'error': 'Комментарий обязателен для отклонения заявления.'},
                            status=status.HTTP_400_BAD_REQUEST)

        reviewer_comment = ApplicationComment.objects.create(user=user, text=comment_text)
        application.reviewer_comment = reviewer_comment
        application.status = Application.Status.REJECTED
        application.save()

        send_status_change_email(application.student.email, application, application.get_status_display())

        serializer = self.get_serializer(application)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated],
            parser_classes=[MultiPartParser, FormParser])
    def upload_document(self, request, pk=None):
        application = self.get_object()
        user = request.user

        sent_document = request.FILES.get('sent_document')
        if not sent_document:
            return Response({'error': 'Файл документа обязателен.'}, status=status.HTTP_400_BAD_REQUEST)

        application.sent_document = sent_document
        application.save()

        send_status_change_email(application.student.email, application, application.get_status_display())

        serializer = self.get_serializer(application)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated],
            parser_classes=[MultiPartParser, FormParser])
    def complete(self, request, pk=None):
        application = self.get_object()
        user = request.user

        ready_document = request.FILES.get('ready_document')
        if not ready_document:
            return Response({'error': 'Файл документа обязателен.'}, status=status.HTTP_400_BAD_REQUEST)

        application.ready_document = ready_document
        application.status = Application.Status.COMPLETED
        application.save()

        send_status_change_email(application.student.email, application, application.get_status_display())

        serializer = self.get_serializer(application)
        return Response(serializer.data)


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


from django.db.models import Case, When, IntegerField

class ProrectorApplicationListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Application.objects.filter(status__in=['in_progress', 'under_review'])
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Возвращает все заявления, сортируя их так, чтобы сперва были те, которые в процессе."""
        return self.queryset.annotate(
            status_order=Case(
                When(status='in_progress', then=0),  # Заявления в процессе будут иметь приоритет (0)
                When(status='under_review', then=1),  # Заявления, которые на проверке, будут вторыми (1)
                output_field=IntegerField(),
            )
        ).order_by('status_order', '-submission_date')



class ReviewApplicationListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Application.objects.filter(status__in=['under_review'])
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
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
