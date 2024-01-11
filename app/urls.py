from django.urls import path

from app.views.company_view import CompanyList, CompanyDetail
from app.views.job_view import JobList, JobDetail

urlpatterns = [
    path('companies/', CompanyList.as_view()),
    path('companies/<int:pk>/', CompanyDetail.as_view()),
    path('jobs/', JobList.as_view()),
    path('jobs/<int:pk>', JobDetail.as_view())
]