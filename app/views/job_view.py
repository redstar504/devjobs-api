import logging

from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from app.logger import logger
from app.models import Job
from app.serializers.job_serializer import JobSerializer, JobDetailSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('id')
    serializer_class = JobSerializer

    def get_queryset(self):
        queryset = Job.objects.all().order_by('id')
        isFulltime = self.request.query_params.get('isFulltime', default="false")

        if isFulltime == 'true':
            logger.debug("[Job Listing] filtering on full time positions")
            queryset = queryset.filter(contract_type="FT")

        return queryset


class JobDetail(APIView):
    def get_object(self, pk):
        try:
            return Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        job = self.get_object(pk)
        serializer = JobDetailSerializer(job)
        return Response(serializer.data)
