from django.urls import path

from app.views.company_view import CompanyList, CompanyDetail
from app.views.job_view import JobDetail, JobViewSet

urlpatterns = [
    path('companies/', CompanyList.as_view(), name="company-list"),
    path('companies/<int:pk>/', CompanyDetail.as_view(), name="company-detail"),
    path('jobs/', JobViewSet.as_view({'get': 'list', 'post': 'create'}), name="job-list"),
    path('jobs/<int:pk>', JobDetail.as_view(), name="job-details"),
]
