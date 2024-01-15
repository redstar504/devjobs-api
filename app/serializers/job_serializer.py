from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from app.models import Job, Company
from app.serializers.company_serializer import CompanySerializer


class JobSerializer(ModelSerializer):
    company_detail = CompanySerializer(source='company', read_only=True)
    company = PrimaryKeyRelatedField(queryset=Company.objects.all(), write_only=True)
    distance = serializers.SerializerMethodField(read_only=True)

    def create(self, validated_data):
        # We are overriding this so we can pick off the city/country and get the coords.
        return Job.objects.create_job(**validated_data)

    def get_distance(self, obj):
        distance = getattr(obj, 'distance', None)
        return round(distance.km) if distance else None

    class Meta:
        model = Job
        fields = ['id', 'company', 'company_detail', 'title', 'description', 'city', 'country', 'contract_type',
                  'post_date', 'distance']


class JobDetailSerializer(ModelSerializer):
    company_detail = CompanySerializer(source='company')

    class Meta:
        model = Job
        fields = ['id', 'company_detail', 'title', 'description', 'city', 'country', 'contract_type', 'post_date']
