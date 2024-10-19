from rest_framework.routers import DefaultRouter
from .views import ApplicationViewSet, ApplicationTypeViewSet, ProrectorApplicationListViewSet

router = DefaultRouter()
router.register(r'list', ApplicationViewSet)
router.register(r'list-for-prorector', ProrectorApplicationListViewSet)
router.register(r'types', ApplicationTypeViewSet, basename='application-types')

urlpatterns = [

]

urlpatterns += router.urls
