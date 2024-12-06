from counsels.models import CounselDocument
from counsels.views import (CounselDetailView, CounselDocumentDetailView,
                            CounselDocumentListCreateView,
                            CounselListCreateView)
from django.urls import path

app_name = "counsels"
urlpatterns = [
    path("", CounselListCreateView.as_view(), name="list"),
    path("<int:pk>/", CounselDetailView.as_view(), name="detail"),
    path(
        "<int:pk>/documents/",
        CounselDocumentListCreateView.as_view(),
        name="counsel_documents",
    ),
    path(
        "<int:customer_pk>/documents/<int:pk>/",
        CounselDocumentDetailView.as_view(),
        name="counsel_document_detail",
    ),
]
