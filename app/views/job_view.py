from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Job
from app.serializers.job_serializer import JobSerializer


class JobList(APIView):
    def get(self, request, format=None):
        jobs = Job.objects.all().order_by("id")
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
