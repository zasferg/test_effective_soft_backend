from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, DishViewSet, ReportViewSet

router = DefaultRouter()
router.register(r"orders", OrderViewSet)
router.register(r"dishes", DishViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("report/", ReportViewSet.as_view()),
]
