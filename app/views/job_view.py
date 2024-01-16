from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.postgres.lookups import SearchLookup
from django.contrib.postgres.search import SearchVector
from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from app.logger import logger
from app.models import Job
from app.serializers.job_serializer import JobSerializer, JobDetailSerializer
from app.util.geocoder import coordinates_from_place_id
from django.db.models import CharField

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('id')
    serializer_class = JobSerializer

    def get_queryset(self):
        queryset = Job.objects.all().order_by('id')
        full_time_only = self.request.query_params.get('fullTimeOnly', default=None)
        keywords = self.request.query_params.get('keywords', default=None)
        place_id = self.request.query_params.get('placeId', default=None)
        longitude = self.request.query_params.get('lng', default=None)
        latitude = self.request.query_params.get('lat', default=None)
        radius = self.request.query_params.get('radius', default=1000)
        search_coords = None

        if longitude is not None and latitude is not None:
            search_coords = (float(longitude), float(latitude))
            logger.debug(f"[JobSearch] geo filter applied {search_coords}:{radius}")

        if place_id is not None:  # todo: complete impl. + caching
            logger.debug(f'[JobSearch] filtering on place ID: {place_id}')
            search_coords = coordinates_from_place_id(place_id)

        if keywords is not None:
            CharField.register_lookup(SearchLookup)
            queryset = queryset.annotate(
                search=SearchVector("title", "description")
            ).filter(search=keywords)

        if full_time_only is not None:
            logger.debug("[JobSearch] filtering on full time positions")
            queryset = queryset.filter(contract_type="FT")

        if search_coords is not None:
            search_point = Point(search_coords[0], search_coords[1], srid=4326)
            queryset = (
                queryset.annotate(distance=Distance("point", search_point))
                .filter(distance__lte=D(km=int(radius)))
                .order_by("distance")
            )

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
