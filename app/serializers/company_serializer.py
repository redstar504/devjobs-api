from rest_framework.serializers import ModelSerializer

from app.models import Company


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'logo', 'color', 'website', 'join_date']
