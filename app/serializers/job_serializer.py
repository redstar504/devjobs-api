from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from app.models import Job, Company, Blurb
from app.serializers.blurb_serializer import BlurbSerializer
from app.serializers.company_serializer import CompanySerializer


class JobSerializer(ModelSerializer):
    company_detail = CompanySerializer(source='company', read_only=True)
    company = PrimaryKeyRelatedField(queryset=Company.objects.all(), write_only=True)

    class Meta:
        model = Job
        fields = ['id', 'company', 'company_detail', 'title', 'description', 'location', 'contract_type']


class JobDetailSerializer(ModelSerializer):
    company_detail = CompanySerializer(source='company')
    blurbs = BlurbSerializer(many=True)

    class Meta:
        model = Job
        fields = ['id', 'company_detail', 'title', 'description', 'location', 'contract_type', 'blurbs']
