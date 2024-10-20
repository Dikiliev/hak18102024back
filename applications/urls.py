from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import ApplicationViewSet, ProrectorApplicationListViewSet, ApplicationTypeViewSet, \
    ProrectorApplicationActionViewSet

# Регистрация стандартных ViewSet-ов в маршрутизаторе
router = DefaultRouter()
router.register(r'list', ApplicationViewSet)
router.register(r'list-for-prorector', ProrectorApplicationListViewSet)
router.register(r'types', ApplicationTypeViewSet, basename='application-types')

# Добавление маршрутов для действий 'sign' и 'reject'
prorector_application_action = ProrectorApplicationActionViewSet.as_view({
    'patch': 'sign'
})
prorector_application_reject = ProrectorApplicationActionViewSet.as_view({
    'patch': 'reject'
})

urlpatterns = [
    # Пример маршрута для подписания заявления
    path('list/<int:pk>/sign/', prorector_application_action, name='application-sign'),

    # Пример маршрута для отклонения заявления
    path('list/<int:pk>/reject/', prorector_application_reject, name='application-reject'),
]

# Добавляем маршруты из router
urlpatterns += router.urls
