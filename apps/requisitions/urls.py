from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import requisitions

app_name = "requisitions"

urlpatterns = [
    path(
        "requisitions/",
        requisitions.RequisitionListView.as_view(),
        name="requisition_list",
    ),
    path(
        "requisitions/<int:pk>/",
        requisitions.RequisitionDetailView.as_view(),
        name="requisition_detail",
    ),
    path(
        "requisitions/<int:pk>/history/",
        requisitions.RequisitionHistoryView.as_view(),
        name="requisition_history",
    ),
]
