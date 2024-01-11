from django.urls import path

from app.views.company_view import CompanyList, CompanyDetail
from app.views.job_view import JobList

urlpatterns = [
    path('companies/', CompanyList.as_view(), name="company-list"),
    path('companies/<int:pk>/', CompanyDetail.as_view(), name="company-detail"),
    path('jobs/', JobList.as_view(), name="job-list")
]