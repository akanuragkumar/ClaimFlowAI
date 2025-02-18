from django.urls import path

from loss_run.views import LossRunUploadView

urlpatterns = [
    path('upload-report/', LossRunUploadView.as_view(), name='loss-upload'),
    # path('<str:customer_uuid>/', CustomerView.as_view(), name='loss_run-details'),
]